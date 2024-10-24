import os
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()


class Config:
    # Flask app configurations
    HOST = os.getenv("FLASK_RUN_HOST", "127.0.0.1")
    PORT = int(os.getenv("FLASK_RUN_PORT", 5000))
    DEBUG = os.getenv("FLASK_DEBUG_MODE")

    OPENAI_APIKEY = os.getenv("OPENAI_APIKEY")
