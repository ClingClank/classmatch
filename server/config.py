import os
from pathlib import Path
from dotenv import load_dotenv

# Load the .env file
env_path = Path(__file__).resolve().parent / ".env"
# Ensure values from server/.env override any existing environment variables
load_dotenv(dotenv_path=env_path, override=True)

DB_USER = os.getenv("DB_USER", "root").strip()
DB_PASS = os.getenv("DB_PASS", "").strip()
DB_HOST = os.getenv("DB_HOST", "localhost").strip()
DB_PORT = os.getenv("DB_PORT", "3306").strip()
DB_NAME = os.getenv("DB_NAME", "classmatch").strip()
