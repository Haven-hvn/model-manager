# Model Manager

A lightweight Python utility to fetch and organize .gguf model files from IPFS.  
Built for [Haven Player](https://github.com/haven-hvn/haven-player) to manage model dependencies seamlessly.

## Features

- Downloads multiple model files from IPFS gateways
- Stores models in organized models/ directory
- Skips already downloaded files
- Structured for import, not CLI

## Installation

```bash
pip install -r requirements.txt

Usage (as a Python package)

`from model_manager.downloader import download_all_models
download_all_models()`

This will download all models defined in config_handler.py into the models/ directory.

Directory Structure

model-manager/
├── model_manager/
│   ├── _init_.py
│   ├── downloader.py
│   └── config_handler.py
├── requirements.txt
└── README.md

Notes

Ensure both .gguf files belonging to a model are in the same folder for LM Studio to load them properly.
