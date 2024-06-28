import os
from dotenv import load_dotenv

load_dotenv()

USTC_PASSPORT_USERNAME = os.environ["USTC_PASSPORT_USERNAME"]
USTC_PASSPORT_PASSWORD = os.environ["USTC_PASSPORT_PASSWORD"]
GITHUB_TOKEN = os.environ["GITHUB_TOKEN"]
LOAD_FROM_FILE = os.getenv("LOAD_FROM_FILE", "False") == "True"
