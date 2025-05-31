import requests
import os
from dotenv import load_dotenv

load_dotenv()
HF_API_TOKEN = os.getenv("HF_API_TOKEN")

API_URL = "https://api-inference.huggingface.co/models/lucataco/comics-diffusion"
headers = {"Authorization": f"Bearer {HF_API_TOKEN}"}

prompt = "A robot knight stands in a burning forest"
payload = {
    "inputs": f"{prompt}, comic style, cel shading, ink outlines",
    "parameters": {
        "negative_prompt": "blurry, low quality, deformed, extra limbs"
    }
}

response = requests.post(API_URL, headers=headers, json=payload)
print("🔁 Status:", response.status_code)

if response.status_code == 200:
    with open("test_image.png", "wb") as f:
        f.write(response.content)
    print("Image saved to test_image.png")
else:
    print("Error:", response.text)