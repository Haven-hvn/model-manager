import os
import json

def save_config(config, save_dir):

    os.makedirs(save_dir, exist_ok=True)
    path = os.path.join(save_dir, "config.json")
    if os.path.exists(path):
        print(f"Config file already exists at {path}. Skipping save.")
        return
    with open(path, "w") as f:
        json.dump(config, f, indent=2)
    print(f"Config saved to {path}")

def load_config(save_dir):
    path = os.path.join(save_dir, "config.json")
    
    with open(path, "r") as f:
        config = json.load(f)
    print(f"Config loaded from {path}")
    
    return config