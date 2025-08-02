from huggingface_hub import hf_hub_download
import os

# script to download mistral model i'm using since github doesnt allow me to commit model file to repo

def download_model():
    os.makedirs("models", exist_ok=True)
    model_path = hf_hub_download(
        repo_id="TheBloke/Mistral-7B-Instruct-v0.2-GGUF",
        filename="mistral-7b-instruct-v0.2.Q4_K_M.gguf",
        local_dir="models"
    )
    print(f"Model downloaded to: {model_path}")

if __name__ == "__main__":
    download_model()