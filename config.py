import os
from dotenv import load_dotenv
from pathlib import Path

# Get absolute path to project root
BASE_DIR = Path(__file__).resolve().parent.parent
ENV_PATH = BASE_DIR / ".env"

# Force load .env
load_dotenv(dotenv_path=ENV_PATH, override=True)

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

print("DEBUG: ENV FILE PATH =", ENV_PATH)
print("DEBUG: GITHUB_TOKEN FOUND =", bool(GITHUB_TOKEN))
print("DEBUG: GROQ_API_KEY FOUND =", bool(GROQ_API_KEY))

if not GITHUB_TOKEN:
    raise ValueError("Missing GITHUB_TOKEN")

if not GROQ_API_KEY:
    raise ValueError("Missing GROQ_API_KEY")



