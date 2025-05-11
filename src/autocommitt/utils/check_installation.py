import os
import platform
import shutil
import subprocess
import requests


def is_ollama_installed():
    """
    Checks if Ollama is installed on the system by verifying its presence in PATH.
    """
    return shutil.which("ollama") is not None


def download_and_install_ollama():
    """
    Downloads and installs Ollama for the appropriate OS.
    """
    # Determine the OS
    system = platform.system().lower()

    # Map OS to Ollama binaries
    download_links = {
        "linux": "https://ollama.com/download/ollama-linux",
        "darwin": "https://ollama.com/download/ollama-macos",
        "windows": "https://ollama.com/download/ollama-windows.exe",
    }

    if system not in download_links:
        raise OSError(f"Unsupported operating system: {system}")

    # Download URL and filename
    download_url = download_links[system]
    filename = f"ollama-{system}" + (".exe" if system == "windows" else "")

    print(f"Downloading Ollama for {system}...")

    # Download the binary
    response = requests.get(download_url, stream=True)
    if response.status_code == 200:
        with open(filename, "wb") as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)
        print(f"Ollama downloaded successfully as '{filename}'.")
    else:
        raise RuntimeError(
            f"Failed to download Ollama. HTTP status code: {response.status_code}"
        )

    # Make executable on Linux/macOS and move to a suitable location
    if system in ["linux", "darwin"]:
        os.chmod(filename, 0o755)
        subprocess.run(["sudo", "mv", filename, "/usr/local/bin/ollama"], check=True)
    elif system == "windows":
        # Add Windows-specific installation steps if necessary
        print(f"Move '{filename}' to a directory in your PATH to use it globally.")
    print("Ollama installation complete.")


# if __name__ == "__main__":
#     if not is_ollama_installed():
#         download_and_install_ollama()
#     else:
#         print("ollama is installed already")
