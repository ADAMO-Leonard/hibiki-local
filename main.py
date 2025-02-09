#!/usr/bin/env python
import sys
import subprocess
from pathlib import Path
import gradio as gr
import time
import os
import glob  # Import glob

# Définition des chemins (absolus)
BASE_DIR = Path(__file__).parent.resolve()
MODEL_DIR = BASE_DIR / "Modeles"
VOICE_DIR = BASE_DIR / "Voix"
VOICE_DIR.mkdir(parents=True, exist_ok=True)

def run_inference(input_audio_path: str, batch_size: int = 2, cfg_coef: float = 3.0):
    """Exécute l'inférence Hibiki, retourne le chemin du fichier audio et la sortie."""
    if not input_audio_path:
        return None, "Erreur : Aucun fichier audio fourni !"

    hibiki_weight = MODEL_DIR / "hibiki-pytorch-220b12c0@200.safetensors"
    mimi_weight = MODEL_DIR / "mimi-pytorch-e351c8d8@125.safetensors"
    tokenizer = MODEL_DIR / "tokenizer_spm_48k_multi6_2.model"
    config = MODEL_DIR / "config.json"

    for file_path in [hibiki_weight, mimi_weight, tokenizer, config]:
        if not file_path.exists():
            return None, f"Erreur : Fichier manquant : {file_path}"

    timestamp = int(time.time())
    output_audio_base = VOICE_DIR / f"translated_audio_{timestamp}"  # Sans extension
    output_audio_pattern = str(output_audio_base) + "*.wav"  # Motif glob

    cmd = [
        sys.executable, "-m", "moshi.run_inference",
        input_audio_path, str(output_audio_base) + ".wav", # Ajout de l'extension
        "--hf-repo", "local",
        "--config", str(config),
        "--tokenizer", str(tokenizer),
        "--moshi-weight", str(hibiki_weight),
        "--mimi-weight", str(mimi_weight),
        "--cfg-coef", str(cfg_coef),
        "--device", "cpu",
        "--batch-size", str(batch_size),
    ]

    print("Exécution de la commande :")
    print(" ".join(cmd))

    try:
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        # Recherche des fichiers correspondant au motif
        matching_files = glob.glob(output_audio_pattern)
        if matching_files:
            # Privilégier le fichier avec "-0"
            for file in matching_files:
                if "-0.wav" in file:
                    return file, result.stdout
            return matching_files[0], result.stdout  # Retourne le premier si pas de "-0"
        else:
            return None, "Aucun fichier audio de sortie trouvé."
    except subprocess.CalledProcessError as e:
        return None, f"Erreur lors de la traduction : {e}\nSortie d'erreur:\n{e.stderr}"
    except FileNotFoundError:
        return None, "Erreur: moshi ou ses dépendances ne sont pas installés."
    except Exception as e:
        return None, f"Erreur inattendue: {e}"

def translate_audio(input_audio, batch_size, cfg_coef):
    """Fonction pour Gradio."""
    if not input_audio:
        return None, "Veuillez sélectionner un fichier audio."

    output_audio_path, transcript = run_inference(input_audio, batch_size, cfg_coef)
    return output_audio_path, transcript

# --- Interface Gradio ---

iface = gr.Interface(
    fn=translate_audio,
    inputs=[
        gr.Audio(label="Audio d'entrée", type="filepath"),
        gr.Slider(minimum=1, maximum=8, step=1, value=2, label="Batch Size"),
        gr.Slider(minimum=1.0, maximum=10.0, step=0.1, value=3.0, label="CFG Coefficient"),
    ],
    outputs=[
        gr.Audio(label="Audio traduit"),
        gr.Textbox(label="Transcription (inclut les logs)", lines=10),
    ],
    title="Traduction audio avec Hibiki (CPU)",
    description="Uploadez un fichier audio et cliquez sur 'Traduire'.",
    allow_flagging="never",
)

if __name__ == "__main__":
    iface.launch()
