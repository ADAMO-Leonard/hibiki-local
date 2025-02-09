# Hibiki : Traduction Vocale Français-Anglais (CPU/GPU)

## Présentation

Hibiki est un projet de traduction *speech-to-speech* (et *speech-to-text*) qui se concentre sur la traduction du français parlé vers l'anglais. Cette version est configurée pour fonctionner sur le CPU et le GPU, avec détection automatique du matériel.

## Installation

1. **Cloner le dépôt :**

    ```bash
    git clone https://github.com/ADAMO-Leonard/hibiki-local.git
    cd hibiki-local
    ```

2. **Créer et activer un environnement Conda :**

    ```bash
    conda create -n hibiki_env python=3.10
    conda activate hibiki_env
    ```

3. **Installer les dépendances :**

    ```bash
    pip install -r requirements.txt
    ```

4. **Télécharger les modèles :**

    ```bash
    python Modeles/download.py
    ```

5. **Vérification GPU :**

    Le système détecte automatiquement si un GPU est disponible. Si votre système dispose d'un GPU compatible, le modèle fonctionnera sur le GPU sans modification supplémentaire.

    **Pour un fonctionnement uniquement sur CPU :**
    
    Si le GPU n'est pas disponible, suivez ces étapes :
    
    - Ouvrez le fichier `quantize.py` dans la librairie `moshi`.
    - Ce fichier se trouve ici :  
      `\anaconda3\envs\hibiki_env\lib\site-packages\moshi\utils\quantize.py`
    
    - Remplacez tout le contenu du fichier par la version fournie dans le dépôt GitHub Hibiki.
      - Vous pouvez soit copier-coller le code, soit télécharger directement le fichier du dépôt Hibiki et remplacer l'original.

6. **Lancer la traduction :**

    ```bash
    python main.py
    ```

## Points à améliorer

Voici quelques améliorations potentielles :

-   [X]  **Interface Gradio :**  Implémenter une interface utilisateur conviviale avec Gradio.
-   [x]  **Accélération GPU :**  Activer la prise en charge du GPU pour un traitement plus rapide.
-   [ ]  **Traduction en temps réel :**  Ajouter une fonctionnalité de traduction en temps réel.

## Remerciements

Nous adressons nos sincères remerciements à :

*   L'**équipe Hibiki** de Kyutai Labs pour le développement de ce projet et sa mise à disposition :
    *   [Dépôt GitHub](https://github.com/kyutai-labs/hibiki)
    *   [Collection Hugging Face](https://huggingface.co/collections/kyutai/hibiki-fr-en-67a48835a3d50ee55d37c2b5)
  

*    Les grands modèles de langage (LLM) qui ont aidé à la rédaction de cette documentation.
