import os
import sys
import requests
import zipfile
import shutil
from urllib.parse import urljoin
from local_version import get_local_version


def get_remote_version(url):
    version_url = urljoin(url, "version.txt")
    response = requests.get(version_url)
    response.raise_for_status()
    return response.text.strip()


def download_and_extract_update(url):
    update_url = urljoin(url, "update.zip")
    response = requests.get(update_url, stream=True)
    response.raise_for_status()

    with open("update.zip", "wb") as f:
        for chunk in response.iter_content(chunk_size=8192):
            f.write(chunk)

    with zipfile.ZipFile("update.zip", "r") as z:
        z.extractall()

    os.remove("update.zip")


def update_app(url):
    local_version = get_local_version()
    remote_version = get_remote_version(url)

    if local_version != remote_version:
        print("Updating...")
        download_and_extract_update(url)
        with open("src/version.txt", "w") as f:
            f.write(remote_version)
        print("Update complete. Restarting...")
        os.execl(sys.executable, sys.executable, *sys.argv)
    else:
        print("Already up to date.")


remote_url = "https://raw.githubusercontent.com/egorskalozub/AI_CopyPaste/main/src"
update_app(remote_url)
