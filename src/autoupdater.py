import os
import sys
import requests
import zipfile
import shutil
from urllib.parse import urljoin
from local_version import get_local_version
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QLabel, QProgressBar, QWidget

VERSION = 'version.txt'
UPDATE = 'update.zip'



def get_remote_version(url):
    version_url = url
    response = requests.get(version_url)
    response.raise_for_status()
    return response.text.strip()


def download_and_extract_update(url, progress_callback):
    update_url = "https://dl.dropboxusercontent.com/s/zmp9cipdigd4lw0/update.zip"  # Replace with your Dropbox direct download link
    response = requests.get(update_url, stream=True)
    response.raise_for_status()

    total_size = int(response.headers.get('content-length', 0))
    downloaded_size = 0

    with open(UPDATE, "wb") as f:
        for chunk in response.iter_content(chunk_size=8192):
            f.write(chunk)
            downloaded_size += len(chunk)
            progress_callback(downloaded_size / total_size * 100)

    with zipfile.ZipFile(UPDATE, "r") as z:
        z.extractall()

    os.remove(UPDATE)


def update_app(url):
    local_version = get_local_version()
    remote_version = get_remote_version(url)

    if local_version != remote_version:
        app = QApplication(sys.argv)
        window = QMainWindow()
        central_widget = QWidget()
        layout = QVBoxLayout()
        central_widget.setLayout(layout)
        window.setCentralWidget(central_widget)

        status_label = QLabel(
            f"Updating from {local_version} to {remote_version}...")
        layout.addWidget(status_label)

        progress_bar = QProgressBar()
        layout.addWidget(progress_bar)

        window.show()

        def progress_callback(progress):
            progress_bar.setValue(progress)

        print("Updating...")
        download_and_extract_update(url, progress_callback)
        with open(VERSION, "w") as f:
            f.write(remote_version)
        print("Update complete. Restarting...")

        sys.exit(app.exec())

    else:
        print("Already up to date.")


remote_url = "https://dl.dropboxusercontent.com/s/jy6dosxieerasxe/version.txt"
update_app(remote_url)


