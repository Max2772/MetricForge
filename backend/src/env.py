import os

from dotenv import load_dotenv

load_dotenv()

LOG_LEVEL: str = (os.getenv("LOG_LEVEL") or "INFO").upper()

API_HOST: str = os.getenv("API_HOST") or "127.0.0.1"
API_PORT: int = int(os.getenv("API_PORT") or 8000)
API_RELOAD: bool = (os.getenv("API_RELOAD").upper() or "TRUE") in ("TRUE", "YES", "ON", "1")
