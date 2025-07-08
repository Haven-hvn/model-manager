# model-manager

A lightweight utility Python module that helps to download and manage Haven player(or similar apps) GGUF models from IPFS.

### Features
- Downloads models using multiple IPFS gateways
- Saves config alongside models
- Handles fallback if a gateway fails
- Asynchronous, non-blocking downloads

### Requirements

```bash
pip install aiohttp aiofiles tqdm

Usage

1. Add model metadata to models.json

2. Run:

python test_downloader.py

Downloaded models and their configs will be saved in:

~/.haven/models/<model_name>/

Structure

model_manager/
├── downloader.py
├── config_handler.py
├── models.json
test_downloader.py

Integration

Import and use in Haven Player or other projects

from model_manager.downloader import download_model