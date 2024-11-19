import os
import pathlib
from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv())

import version

BASE_DIR = pathlib.Path(__file__).resolve().parent

API_TITLE = os.getenv("API_TITLE", "FastAPI Backend Template")
API_PORT = int(os.getenv("API_PORT", "8081"))
API_VERSION = os.getenv("API_VERSION", version.__version__)

API_KEY_NAME = os.getenv("API_KEY_NAME", "x-api-key")
API_KEY = os.getenv("API_KEY", "dummy")
