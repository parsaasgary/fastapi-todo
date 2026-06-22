import sys
from pathlib import Path

def get_base_dir():
    if getattr(sys, 'frozen', False):
        # Running as EXE → use the folder where the .exe is located
        return Path(sys.executable).resolve().parent
    else:
        # Running from source
        return Path(__file__).resolve().parent
    

BASE_DIR = get_base_dir()

CREDENTIALS_DIR = BASE_DIR / "confg"

CREDENTIALS_EVV_DIR = CREDENTIALS_DIR / "credentials.env"