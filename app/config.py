import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    APP_NAME = "ClariCart Decision Engine"
    APP_VERSION = "1.0.0"

    EXTERNAL_API_URL = os.getenv("EXTERNAL_API_URL")
    EXTERNAL_API_KEY = os.getenv("EXTERNAL_API_KEY")

settings = Settings()