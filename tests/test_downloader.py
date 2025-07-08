import os
import json
import sys

# Allow importing from model_manager/
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'model_manager')))

from model_manager.downloader import download_model  # same function, reused
from model_manager.config_handler import save_config, load_config

# Set model name and path to models.json
MODEL_NAME = "haven-vlm-v2"
MODELS_JSON_PATH = "model_manager/models.json"

# Load models.json 
if not os.path.exists(MODELS_JSON_PATH):
    print(f" models.json not found at {MODELS_JSON_PATH}")
    exit(1)

with open(MODELS_JSON_PATH, "r") as f:
    models = json.load(f)

# Check if the model exists in models.json
if MODEL_NAME not in models:
    print(f" Model '{MODEL_NAME}' not found in models.json.")
    exit(1)

# Extract model details
model_entry = models[MODEL_NAME]
config = model_entry["config"]
files = model_entry.get("files") 

#  Create model save directory
model_dir = os.path.expanduser(f"~/.haven/models/{MODEL_NAME}")
os.makedirs(model_dir, exist_ok=True)

# Download logic (support single or multiple .gguf files)
if files:  # multiple files
    for file_info in files:
        filename = file_info["filename"]
        cid = file_info["cid"]
        print(f" Downloading: {filename}")
        download_model(MODEL_NAME, cid, model_dir, filename=filename)
else:  # fallback to single file logic
    cid = model_entry["cid"]
    filename = config.get("filename", "model.bin")
    print(f" Downloading model '{MODEL_NAME}' from CID: {cid}")
    download_model(MODEL_NAME, cid, model_dir, filename=filename)

# Save model config
save_config(config, model_dir)

# Load and print config to verify
loaded = load_config(model_dir)
if loaded:
    print(f" Loaded config:\n{json.dumps(loaded, indent=2)}")
else:
    print("  Config not found or failed to load.")