import os
import requests
import logging
from typing import List
from model_manager.config_handler import default_models

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

class DownloadError(Exception):
    """Custom exception raised when download fails from all gateways."""
    pass


def build_gateway_links(cid: str, filename: str) -> List[str]:
    """Generate IPFS gateway URLs from CID."""
    return [
        f"https://{cid}.ipfs.w3s.link/?filename={filename}",
        f"https://ipfs.io/ipfs/{cid}?filename={filename}",
        f"https://cloudflare-ipfs.com/ipfs/{cid}?filename={filename}"
    ]


def download_file(urls: List[str], output_path: str) -> None:
    for url in urls:
        try:
            logger.info(f" Trying {url}")
            with requests.get(url, stream=True, timeout=20) as response:
                response.raise_for_status()
                os.makedirs(os.path.dirname(output_path), exist_ok=True)
                with open(output_path, "wb") as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        if chunk:
                            f.write(chunk)
            logger.info(f" Downloaded to {output_path}")
            return
        except Exception as e:
            logger.warning(f" Failed: {e}")
    raise DownloadError(f" All download attempts failed for {output_path}")


def download_all_models():
    """Go through the config and download all listed models."""
    for model_id, model_files in default_models.items():
        model_dir = os.path.join("models", model_id)
        logger.info(f" Processing model: {model_id}")
        for file_info in model_files:
            filename = file_info["filename"]
            cid = file_info["cid"]
            output_path = os.path.join(model_dir, filename)

            if os.path.exists(output_path):
                logger.info(f" Already exists: {output_path}")
                continue

            gateways = build_gateway_links(cid, filename)
            try:
                download_file(gateways, output_path)
            except DownloadError as e:
                logger.error(str(e))

