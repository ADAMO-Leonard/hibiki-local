import os
import requests

# Dossier des modèles
MODEL_DIR = os.path.dirname(__file__)

# URLs des fichiers à télécharger
FILES = {
    "hibiki": "https://huggingface.co/kyutai/hibiki-2b-pytorch-bf16/resolve/main/hibiki-pytorch-220b12c0@200.safetensors",
    "mimi": "https://huggingface.co/kyutai/hibiki-2b-pytorch-bf16/resolve/main/mimi-pytorch-e351c8d8@125.safetensors",
    "tokenizer": "https://huggingface.co/kyutai/hibiki-2b-pytorch-bf16/resolve/main/tokenizer_spm_48k_multi6_2.model",
    "config": "https://huggingface.co/kyutai/hibiki-2b-pytorch-bf16/resolve/main/config.json",
}

def download_file(url, dest):
    """Télécharge un fichier si non présent."""
    if not os.path.exists(dest):
        print(f"Téléchargement de {os.path.basename(dest)}...")
        response = requests.get(url, stream=True)
        response.raise_for_status()  # Vérifie si la requête a réussi
        with open(dest, "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        print(f"{os.path.basename(dest)} téléchargé avec succès.")
    else:
        print(f"{os.path.basename(dest)} est déjà présent.")

if __name__ == "__main__":
    os.makedirs(MODEL_DIR, exist_ok=True)
    for name, url in FILES.items():
        file_name = url.split("/")[-1]
        download_file(url, os.path.join(MODEL_DIR, file_name))

