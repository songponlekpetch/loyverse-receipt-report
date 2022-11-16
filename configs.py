from dotenv import load_dotenv
import os
from pathlib import Path

env_path = Path(str(Path(".env").resolve()))
load_dotenv(dotenv_path=env_path)

GIT_HASH = os.getenv("GIT_HASH", "unknown")

GOOGLE_APPLICATION_CREDENTIALS = os.getenv("GOOGLE_APPLICATION_CREDENTIALS", "credentials/service_account.json")
GOOGLE_SHEET_URL = os.getenv("GOOGLE_SHEET_URL")

LOYVERSE_URL = "https://api.loyverse.com/v1.0"
LOYVERSE_TOKEN = "cfe6dd803e0e4bf3831ceebca57c6d6f"
API_PATH = {
    "GET_RECEIPTS": "/receipts",
    "GET_CUSTOMERS": "/customers",
    "GET_POST_DEVICES": "/pos_devices",
    "GET_STORES": "/stores",
    "GET_ITEMS": "/items",
    "GET_CATEGORIES": "/categories",
    "GET_EMPLOYEES": "/employees"
}
