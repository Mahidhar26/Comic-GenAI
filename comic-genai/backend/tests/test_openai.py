import os
from dotenv import load_dotenv
from openai import OpenAI

# Force loading the .env file from backend/
dotenv_path = os.path.join(os.path.dirname(__file__), "../backend/.env")
load_dotenv(dotenv_path)

api_key = os.getenv("OPENAI_API_KEY")
print("🔑 API KEY FOUND:", bool(api_key))  # Should print True

client = OpenAI(api_key=api_key)

response = client.models.list()
print("✅ Available models:")
for model in response.data:
    print("-", model.id)