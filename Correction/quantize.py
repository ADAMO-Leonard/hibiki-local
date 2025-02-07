# Copyright (c) Kyutai, all rights reserved.
# This source code is licensed under the license found in the
# LICENSE file in the root directory of this source tree.

"""Fallback pour la quantification (initialement basée sur bitsandbytes).
Cette version supprime la dépendance à bitsandbytes et effectue des opérations linéaires
classiques avec torch.nn.functional.linear. Le comportement quantifié spécifique n'est pas reproduit.
"""

import torch
from torch import nn
import torch.nn.functional as F

def is_quantized(module: nn.Module, name: str = 'weight'):
    """Retourne True si le module possède un attribut '<name>_scb' (indiquant qu'il a été quantifié)."""
    return hasattr(module, name + '_scb')


def linear(module: nn.Module, x: torch.Tensor, name='weight') -> torch.Tensor:
    """
    Applique une opération linéaire.
    Si le module est quantifié, on effectue un fallback en half precision.
    """
    if is_quantized(module, name):
        print("Warning: fallback linear for quantized module (bitsandbytes not available).")
        weight = getattr(module, name)
        return F.linear(x.half(), weight.half())
    else:
        return F.linear(x, getattr(module, name))


def multi_linear(num_steps: int, schedule: list[int] | None,
                 module: nn.Module, x: torch.Tensor, offset: int, name='weight') -> torch.Tensor:
    """
    Applique une couche linéaire multiple à l'entrée.
    Pour chaque pas de temps, une tranche du poids est utilisée.
    
    Args:
        num_steps (int): Nombre total de pas de temps possibles.
        schedule (list[int] ou None): Calendrier de partage des poids.
        module (nn.Module): Module contenant le poids (et éventuellement le paramètre '_scb').
        x (torch.Tensor): Tenseur d'entrée de forme [B, T, C].
        offset (int): Décalage pour le pas de temps courant.
        name (str): Nom de l'attribut contenant le poids (par défaut 'weight').
    """
    B, T, C = x.shape
    ys: list[torch.Tensor] = []
    if is_quantized(module, name):
        weight = getattr(module, name)
        weight_scb = getattr(module, name + '_scb')
    else:
        weight = getattr(module, name)
        weight_scb = None
    assert isinstance(weight, torch.Tensor)

    num_linear = num_steps if schedule is None else max(schedule) + 1

    chout, chin = weight.shape
    weight = weight.view(num_linear, -1, chin)
    if weight_scb is not None:
        # On s'assure que la forme est cohérente
        assert weight_scb.shape == (chout,), (weight_scb, chout)
        weight_scb = weight_scb.view(num_linear, -1)
        assert weight_scb.dtype == torch.float, weight_scb.dtype

    for t in range(T):
        linear_index = t + offset
        if schedule is not None:
            linear_index = schedule[linear_index]
        if weight_scb is None:
            y = F.linear(x[:, t], weight[linear_index])
        else:
            # Fallback : utilisation d'une opération linéaire classique en half precision
            y = F.linear(x[:, t].half(), weight[linear_index].half())
        ys.append(y)
    out = torch.stack(ys, 1)
    return out


def quantize_param(module: nn.Module, name: str = 'weight') -> None:
    """
    Fait un 'quantize' du paramètre donné.
    Dans ce fallback, si bitsandbytes n'est pas disponible, on affiche un avertissement
    et on ne modifie pas les poids.
    """
    if is_quantized(module, name):
        # Si le module est déjà quantifié, on vérifie que SCB est en float
        SCB = getattr(module, name + '_scb')
        if SCB.dtype != torch.float:
            setattr(module, name + '_scb', nn.Parameter(SCB.to(torch.float), requires_grad=False))
        return
    weight = getattr(module, name)
    assert weight.data.dtype.is_floating_point
    print("Warning: quantization fallback - skipping advanced quantization (bitsandbytes not available).")
    # Ici, nous ne réalisons pas de quantification réelle. On laisse weight tel quel,
    # et on crée un SCB factice (par exemple, un tenseur de 1) pour respecter l'interface.
    setattr(module, name, nn.Parameter(weight.data, requires_grad=False))
    scb = torch.ones(weight.shape[0], dtype=torch.float, device=weight.device)
    setattr(module, name + '_scb', nn.Parameter(scb, requires_grad=False))


def quantize_linear(linear: nn.Module) -> None:
    """
    Quantifie une couche linéaire en s'assurant qu'il n'y a pas de biais.
    Dans ce fallback, on applique quantize_param.
    """
    assert linear.bias is None, "Le module linéaire ne doit pas avoir de biais pour la quantification."
    quantize_param(linear)
