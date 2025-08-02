from huggingface_hub import hf_hub_download
import os

# Script to download Mistral model, with optional skip for deployment/testing

REPO_ID = "TheBloke/Mistral-7B-Instruct-v0.2-GGUF"
FILENAME = "mistral-7b-instruct-v0.2.Q4_K_M.gguf"
MODEL_DIR = "models"

def download_model():
    os.makedirs(MODEL_DIR, exist_ok=True)
    model_path = os.path.join(MODEL_DIR, FILENAME)

    # Skip download if file exists
    if os.path.exists(model_path):
        print(f"Model already exists at {model_path}. Skipping download.")
        return

    # Optional: Skip download entirely for testing/deployment via env variable
    if os.getenv("SKIP_MODEL_DOWNLOAD", "false").lower() == "true":
        print("Skipping model download due to SKIP_MODEL_DOWNLOAD flag.")
        return

    print(f"Downloading model from {REPO_ID}/{FILENAME} ...")
    try:
        hf_hub_download(
            repo_id=REPO_ID,
            filename=FILENAME,
            local_dir=MODEL_DIR,
            local_dir_use_symlinks=False  # Ensure actual copy, no symlink
        )
        print("✅ Model download complete.")
    except Exception as e:
        print(f"❌ Failed to download model: {e}")

if __name__ == "__main__":
    download_model()
