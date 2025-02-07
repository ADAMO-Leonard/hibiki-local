# Hibiki: French-English Speech Translation (CPU)

## Overview

Hibiki is a speech-to-speech (and speech-to-text) translation project that focuses on translating spoken French to English. This version is configured to run on the CPU.

## Installation

1.  **Clone the Repository:**

    ```bash
    git clone https://github.com/kyutai-labs/hibiki.git
    cd hibiki
    ```

2.  **Create and Activate a Conda Environment:**

    ```bash
    conda create -n hibiki_env python=3.10
    conda activate hibiki_env
    ```

3.  **Install Dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

4.  **Download the Models:**

    ```bash
    python Modèles/download.py
    ```

5.  **Important:  CPU Compatibility Fix (Moshi Library)**

    To make Hibiki work correctly on the CPU, you need to replace the original `quantize.py` file in the `moshi` library with the version provided in the Hibiki GitHub repository.  This is crucial for CPU operation.

    Locate the file here:
    `\anaconda3\envs\hibiki_env\lib\site-packages\moshi\utils\quantize.py`

   Replace its entire content with the `quantize.py` from the Hibiki repository.  You can either copy and paste the code or download the file directly and replace the original. There's not git clone because it's a specific file in the repository.

6.  **Run the Translation:**

    ```bash
    python main.py
    ```

## Areas for Improvement

Here are some potential enhancements:

-   [ ]  **Gradio Interface:**  Implement a user-friendly interface using Gradio.
-   [ ]  **GPU Acceleration:**  Enable GPU support for faster processing.
-   [ ]  **Real-time Translation:**  Add functionality for real-time translation.

## Acknowledgements

We extend our sincere gratitude to:

*   The **Hibiki team** at Kyutai Labs for developing this project and making it available:
    *   [GitHub Repository](https://github.com/kyutai-labs/hibiki)
    *   [Hugging Face Collection](https://huggingface.co/collections/kyutai/hibiki-fr-en-67a48835a3d50ee55d37c2b5)
*   The Large Language Models (LLMs) that assisted in writing this documentation.
