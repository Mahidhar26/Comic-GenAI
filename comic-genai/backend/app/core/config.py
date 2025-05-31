from functools import lru_cache
from pydantic import BaseModel
from dotenv import load_dotenv
import os

# Load from same backend folder as this file
env_path = os.path.join(os.path.dirname(__file__), "../../.env")
load_dotenv(env_path)

class Settings(BaseModel):
    openai_key: str = os.getenv("OPENAI_API_KEY", "")

@lru_cache
def get_settings():
    return Settings()
