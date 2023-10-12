import os
import requests
from tqdm import tqdm
import torch

def download_models():
    # Create a directory to save the files
    if not os.path.exists("gpt4all"):
        os.makedirs("gpt4all")

    base_directory = "models_TTS"

    # URLs of the files to download
    gpt4all_urls  = [
        "https://gpt4all.io/models/wizardlm-13b-v1.1-superhot-8k.ggmlv3.q4_0.bin",
        "https://huggingface.co/nomic-ai/gpt4all-falcon-ggml/resolve/main/ggml-model-gpt4all-falcon-q4_0.bin",
        "https://huggingface.co/TheBloke/Nous-Hermes-13B-GGML/resolve/main/nous-hermes-13b.ggmlv3.q4_0.bin",
        "https://huggingface.co/TheBloke/GPT4All-13B-snoozy-GGML/resolve/main/GPT4All-13B-snoozy.ggmlv3.q4_0.bin",
        "https://huggingface.co/TheBloke/orca_mini_7B-GGML/resolve/main/orca-mini-7b.ggmlv3.q4_0.bin",
        "https://huggingface.co/TheBloke/orca_mini_3B-GGML/resolve/main/orca-mini-3b.ggmlv3.q4_0.bin",
        "https://huggingface.co/TheBloke/orca_mini_13B-GGML/resolve/main/orca-mini-13b.ggmlv3.q4_0.bin",
        "https://huggingface.co/TheBloke/WizardLM-13B-Uncensored-GGML/resolve/main/wizardLM-13B-Uncensored.ggmlv3.q4_0.bin",
        "https://huggingface.co/nomic-ai/ggml-replit-code-v1-3b/resolve/main/ggml-replit-code-v1-3b.bin",
        "https://gpt4all.io/models/ggml-all-MiniLM-L6-v2-f16.bin",
        "https://gpt4all.io/models/starcoderbase-3b-ggml.bin",
        "https://gpt4all.io/models/starcoderbase-7b-ggml.bin",
        "https://huggingface.co/TheBloke/Llama-2-7B-Chat-GGML/resolve/main/llama-2-7b-chat.ggmlv3.q4_0.bin"
    ]

    # URLs of the language models to download
    language_models = [
        "ru", "ua", "uz", "indic", "en", "de", "es", "fr"
    ]

    # Download and save the GPT-4ALL models with progress display
    for url in gpt4all_urls:
        file_name = os.path.join("gpt4all", os.path.basename(url))
        if not os.path.exists(file_name):
            response = requests.get(url, stream=True)
            if response.status_code == 200:
                total_size = int(response.headers.get("content-length", 0))
                with open(file_name, "wb") as file, tqdm(
                    total=total_size, unit="B", unit_scale=True, unit_divisor=1024
                ) as progress_bar:
                    for data in response.iter_content(chunk_size=1024):
                        file.write(data)
                        progress_bar.update(len(data))
                print(f"Downloaded: {file_name}")
            else:
                print(f"Failed to download: {url}")
        else:
            print(f"File already exists: {file_name}")

    # Load language models
    device = torch.device('cpu')
    torch.set_num_threads(4)

    for language in language_models:
        local_file = os.path.join(base_directory, f'model_{language}.pt')
        folder_path = os.path.dirname(local_file)

        # Check if the folder exists and create it if not
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)

        if not os.path.isfile(local_file):
            url = f'https://models.silero.ai/models/tts/{language}/v4_{language}.pt'

            if language in ["en", "en_indic", "de", "es", "fr"]:
                url = f'https://models.silero.ai/models/tts/{language}/v3_{language}.pt'

            response = torch.hub.download_url_to_file(url, local_file, progress=True)

        model = torch.package.PackageImporter(local_file).load_pickle("tts_models", "model")
        model.to(device)

        print(f"Model for {language} downloaded and loaded.")