from diffusers import DiffusionPipeline
import torch
import uuid
import os
from PIL import Image, ImageDraw, ImageFont

# Load the pipeline once
pipe = DiffusionPipeline.from_pretrained(
    "ogkalu/Comic-Diffusion",
    torch_dtype=torch.float32  # Use float16 for GPU
)
pipe = pipe.to("cuda" if torch.cuda.is_available() else "cpu")

def generate_image(prompt: str, dialogue: str = "", position: str = "bottom-left") -> str:
    image = pipe(prompt).images[0]
    if dialogue:
        image = overlay_dialogue(image, dialogue, position)

    filename = f"panel_{uuid.uuid4().hex[:8]}.png"
    path = os.path.join("static", filename)
    image.save(path)
    return f"/static/{filename}"


def overlay_dialogue(image: Image.Image, text: str, position="bottom-left") -> Image.Image:
    draw = ImageDraw.Draw(image)
    try:
        font = ImageFont.truetype("arial.ttf", 24)  # Update path if needed
    except:
        font = ImageFont.load_default()

    # Set position
    padding = 10
    width, height = image.size
    text_width, text_height = draw.textsize(text, font=font)

    if position == "bottom-left":
        x = padding
        y = height - text_height - padding
    elif position == "top-left":
        x = padding
        y = padding
    elif position == "top-right":
        x = width - text_width - padding
        y = padding
    elif position == "bottom-right":
        x = width - text_width - padding
        y = height - text_height - padding
    else:
        x = padding
        y = height - text_height - padding

    # Draw background box
    draw.rectangle(
        [x - 5, y - 5, x + text_width + 5, y + text_height + 5],
        fill=(0, 0, 0, 180)
    )
    draw.text((x, y), text, fill="white", font=font)
    return image
# def generate_image(prompt: str) -> str:
#     payload = {
#         "inputs": f"{prompt}, comic book illustration, line art, inked outlines, high detail",
#         "parameters": {
#             "negative_prompt": "blurry, watermark, distorted, bad anatomy"
#         }
#     }

#     response = requests.post(API_URL, headers=HEADERS, json=payload)
#     print("📡 HF Status:", response.status_code)
#     if response.status_code != 200:
#         raise Exception(f"Hugging Face API Error {response.status_code}: {response.text}")

#     image_data = response.content
#     output_path = "generated_panel.png"
#     with open(output_path, "wb") as f:
#         f.write(image_data)

#     return f"/static/{output_path}"