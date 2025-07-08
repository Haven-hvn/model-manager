import os
import asyncio
import aiohttp
from pypdl.downloader import Singledown
import aiofiles
from tqdm import tqdm


# IPFS Gateways
IPFS_GATEWAYS = [
    "https://ipfs.io/ipfs/",
    "https://cloudflare-ipfs.com/ipfs/",
    "https://storacha.link/ipfs/",
    "https://gateway.pinata.cloud/ipfs/",
    "https://{cid}.ipfs.w3s.link/",  # fallback-style URL
]

async def try_gateway(url, save_path):
    """
    Try downloading from a single gateway.
    Returns True on success, False on error.
    """
    try:
        async with aiohttp.ClientSession() as session:
            print(f" Starting download stream from: {url}")
            async with session.get(url) as response:
                if response.status != 200:
                    raise Exception(f"Status code: {response.status}")

                total = int(response.headers.get("Content-Length", 0))
                print(f"Downloading: {os.basename(save_path)}")
                if total:
                      print(f"🧩Model file size: {total / 1_048_576:.2f} MB")
                else:
                      print("🧩Model file size: Unknown (Content-Length not provided)")

                downloaded = 0
                progress = tqdm(

                    total=int(response.headers.get("Content-Length", 0)) or None,
                    unit='B',
                    unit_scale=True,
                    desc="Downloading",
                )

                async with aiofiles.open(save_path, 'wb') as f:
                    async for chunk in response.content.iter_chunked(1024 * 1024):
                        await f.write(chunk)
                        downloaded += len(chunk)
                        progress.update(len(chunk))
                        progress.set_postfix({"Downloaded": f"{downloaded / 1_048_576:.2f} MB"})
                progress.close()

        return True

    except Exception as e:
        print(f" Failed to download, trying next gateway.")
        return False

def download_model(model_name, cid, save_dir, filename="model.gguf"):
    """
    Downloads a model from IPFS using fallback gateways.
    """
    os.makedirs(save_dir, exist_ok=True)
    save_path = os.path.join(save_dir, filename)

    print(f" Attempting to download model '{model_name}' from IPFS CID: {cid}")

    # Try each gateway one by one
    for gateway in IPFS_GATEWAYS:
        if "{cid}" in gateway:
            url = gateway.replace("{cid}", cid) + f"?filename={filename}"
        else:
            url = gateway + cid + f"/{filename}"

        print(f"Trying: {url}")
        success = asyncio.run(try_gateway(url, save_path))
        if success:
            print(f" Successfully downloaded '{os.basename(save_path)}' from: {url}")

            return save_path

    print("All gateways failed. Could not download the model.")
    return None

def download_model_files(model_name, files, save_dir):
    """
    Downloads all model files listed under 'files' into the same directory.
    
    Args:
        model_name (str): The name of the model.
        files (list): A list of dicts with 'filename' and 'cid' keys.
        save_dir (str): The directory where the model files will be saved.
    """
    os.makedirs(save_dir, exist_ok=True)

    for file in files:
        filename = file["filename"]
        cid = file["cid"]

        print(f"\nDownloading file: {filename}")
        download_model(model_name, cid, save_dir, filename=filename)