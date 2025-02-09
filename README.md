[![Français](https://img.shields.io/badge/README-Français-blue.svg)](ReadmeFR.md)

# Hibiki: French-English Speech Translation (CPU/GPU)

## Overview

Hibiki is a speech-to-speech (and speech-to-text) translation project that focuses on translating spoken French to English. This version is configured to run on both CPU and GPU, with automatic detection of hardware.

## Installation

1. **Clone the Repository:**

    ```bash
    git clone https://github.com/ADAMO-Leonard/hibiki-local.git
    cd hibiki-local
    ```

2. **Create and Activate a Conda Environment:**

    ```bash
    conda create -n hibiki_env python=3.10
    conda activate hibiki_env
    ```

3. **Install Dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

4. **Download the Models:**

    ```bash
    python Modeles/download.py
    ```
5. **Run the Translation:**

    ```bash
    python main.py
    ```

6. **Check for GPU:**

    The system will automatically detect if a GPU is available. If your system has a compatible GPU, the model will run on the GPU without any further modification.

    **For CPU-only operation:**
    
    If the GPU is not available, follow these steps:
    
    - Open the `quantize.py` file in the `moshi` library.
    - This file can be found here:  
      `\anaconda3\envs\hibiki_env\lib\site-packages\moshi\utils\quantize.py`
    
    - Replace the entire content of the file with the version provided in the Hibiki GitHub repository.
      - You can either copy-paste the code or download the file directly from the Hibiki repository and replace the original.



## Areas for Improvement

Here are some potential enhancements:

-   [x]  **Gradio Interface:**  Implement a user-friendly interface using Gradio.
-   [x]  **GPU Acceleration:**  Enable GPU support for faster processing.
-   [ ]  **Real-time Translation:**  Add functionality for real-time translation.

## Acknowledgements

We extend our sincere gratitude to:

*   The **Hibiki team** at Kyutai Labs for developing this project and making it available:
    *   [GitHub Repository](https://github.com/kyutai-labs/hibiki)
    *   [Hugging Face Collection](https://huggingface.co/collections/kyutai/hibiki-fr-en-67a48835a3d50ee55d37c2b5)
*   The Large Language Models (LLMs) that assisted in writing this documentation.
