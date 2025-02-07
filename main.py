#!/usr/bin/env python
import sys
import subprocess
from pathlib import Path

# Définition des chemins
MODEL_DIR = Path("Modeles")
VOICE_DIR = Path("Voix")

def run_inference(input_audio: Path, output_audio: Path, batch_size: int = 2, cfg_coef: float = 3.0):
    # Chemins vers les fichiers locaux
    hibiki_weight = MODEL_DIR / "hibiki-pytorch-220b12c0@200.safetensors"
    mimi_weight   = MODEL_DIR / "mimi-pytorch-e351c8d8@125.safetensors"
    tokenizer     = MODEL_DIR / "tokenizer_spm_48k_multi6_2.model"
    config        = MODEL_DIR / "config.json"

    # Construction de la commande d'inférence en forçant l'utilisation du CPU
    cmd = [
        sys.executable, "-m", "moshi.run_inference",
        str(input_audio), str(output_audio),
        "--hf-repo", "local",                # On utilise des fichiers locaux
        "--config", str(config),
        "--tokenizer", str(tokenizer),
        "--moshi-weight", str(hibiki_weight),  # Fichier de poids Hibiki
        "--mimi-weight", str(mimi_weight),     # Fichier de poids Mimi
        "--cfg-coef", str(cfg_coef),
        "--device", "cpu",                     # Forcer l'utilisation du CPU
        "--batch-size", str(batch_size),
    ]

    print("Exécution de la commande :")
    print(" ".join(cmd))
    subprocess.run(cmd, check=True)

def main():
    # On définit les chemins d'entrée et de sortie dans le dossier Voix
    audio_in = Path("Voix") / "sample_audio.mp3"
    audio_out = Path("Voix") / "translated_audio.wav"

    if not audio_in.exists():
        print(f"Erreur : {audio_in} n'existe pas ! Ajoutez un fichier audio dans le dossier Voix.")
        sys.exit(1)

    run_inference(audio_in, audio_out)
    print(f"Traduction terminée. Fichier de sortie : {audio_out}")

if __name__ == "__main__":
    main()
