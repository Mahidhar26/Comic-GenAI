# from fastapi import FastAPI, HTTPException
# from app.models.request import StoryRequest
# # from app.models.storyboard import Storyboard
# # from app.services.storyboard import generate_storyboard
# # from fastapi.middleware.cors import CORSMiddleware
# # from fastapi import Body
# # from app.services.imagegen import generate_image
# # from fastapi.staticfiles import StaticFiles
# # from fastapi import FastAPI, Request
# # from fastapi.responses import JSONResponse
# # from diffusers import DiffusionPipeline
# # import torch
# # from PIL import Image, ImageDraw, ImageFont
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from diffusers import DiffusionPipeline
from PIL import Image, ImageDraw, ImageFont
from diffusers import StableDiffusionPipeline
import torch
import os
import uuid

app = FastAPI(title="ComicGen API")
app.mount("/static", StaticFiles(directory="static"), name="static")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="."), name="static")

# pipe = DiffusionPipeline.from_pretrained("ogkalu/Comic-Diffusion", torch_dtype=torch.float32)
pipe = StableDiffusionPipeline.from_pretrained("runwayml/stable-diffusion-v1-5", torch_dtype=torch.float32)
# pipe = DiffusionPipeline.from_pretrained("CompVis/stable-diffusion-v1-4", torch_dtype=torch.float32)
pipe.to("cpu")

def overlay_dialogue(image: Image.Image, text: str, position: str = "bottom-left") -> Image.Image:
    draw = ImageDraw.Draw(image)
    font = ImageFont.load_default()

    if not isinstance(text, str):
        text = str(text) if text is not None else ""

    try:
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
    except AttributeError:
        text_width, text_height = draw.textsize(text, font=font)

    padding = 10
    margin = 20

    if position == "top-left":
        x = margin
        y = margin
    elif position == "top-right":
        x = image.width - text_width - 2 * padding - margin
        y = margin
    else:
        x = margin
        y = image.height - text_height - 2 * padding - margin

    bubble_box = [x - padding, y - padding, x + text_width + padding, y + text_height + padding]
    draw.rectangle(bubble_box, fill=(255, 255, 255, 200))
    draw.text((x, y), text, fill="black", font=font)

    return image

def generate_image(prompt: str, dialogue: str = "", position: str = "bottom-left") -> str:
    image = pipe(prompt).images[0]
    if dialogue:
        image = overlay_dialogue(image, dialogue, position)

    filename = f"panel_{uuid.uuid4().hex[:8]}.png"

    # Ensure static directory exists
    os.makedirs("static", exist_ok=True)

    path = os.path.join("static", filename)
    image.save(path)

    # This will result in the URL /static/filename
    return f"/static/{filename}"

@app.post("/generate-image")
async def generate_image_endpoint(request: Request):
    try:
        data = await request.json()
        scene = data.get("scene")
        dialogue = data.get("dialogue", "")
        position = data.get("position", "bottom-left")

        if not scene:
            return JSONResponse(status_code=400, content={"error": "Missing 'scene' field"})

        image_path = generate_image(scene, dialogue, position)
        return {"image": image_path}
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})


# pipe = DiffusionPipeline.from_pretrained("ogkalu/Comic-Diffusion", torch_dtype=torch.float32)
# pipe.to("cpu")  # or .to("cuda") if GPU available
# app = FastAPI(title="ComicGen API")
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["http://localhost:3000"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )
# app.mount("/static", StaticFiles(directory="."), name="static")

# @app.post("/storyboard", response_model=Storyboard)
# async def storyboard(req: StoryRequest):
#     print("🔍 Received request:", req)
#     try:
#         return generate_storyboard(req.text, req.panel_count)
#     except Exception as exc:
#         print("Exception:", exc)
#         raise HTTPException(status_code=400, detail=str(exc))

# def overlay_dialogue(image: Image.Image, text: str, position: str = "bottom-left") -> Image.Image:
#     draw = ImageDraw.Draw(image)
#     font = ImageFont.load_default()

#     # Use textbbox to calculate the size of the speech bubble
#     bbox = draw.textbbox((0, 0), text, font=font)
#     text_width = bbox[2] - bbox[0]
#     text_height = bbox[3] - bbox[1]
    
#     padding = 10
#     margin = 20

#     # Positioning
#     if position == "top-left":
#         x = margin
#         y = margin
#     elif position == "top-right":
#         x = image.width - text_width - 2 * padding - margin
#         y = margin
#     else:  # bottom-left
#         x = margin
#         y = image.height - text_height - 2 * padding - margin

#     # Draw bubble
#     bubble_box = [x - padding, y - padding, x + text_width + padding, y + text_height + padding]
#     draw.rectangle(bubble_box, fill=(255, 255, 255, 200))

#     # Draw text
#     draw.text((x, y), text, fill="black", font=font)

#     return image

# def generate_image(prompt: str, dialogue: str = "", position: str = "bottom-left") -> str:
#     image = pipe(prompt).images[0]
#     if dialogue:
#         image = overlay_dialogue(image, dialogue, position)
    
#     filename = f"panel_{uuid.uuid4().hex[:8]}.png"
#     path = os.path.join("static", filename)
#     image.save(path)
#     return f"/static/{filename}"

# @app.post("/generate-comic")
# async def generate_comic(request: Request):
#     try:
#         data = await request.json()
#         text = data.get("text")
#         panel_count = data.get("panel_count", 4)

#         if not text:
#             return JSONResponse(status_code=400, content={"error": "Missing 'text' field"})

#         # Step 1: Generate storyboard panels (description, dialogue tuples)
#         panels = generate_storyboard(text, panel_count)

#         # Step 2: Generate images and assemble response
#         results = []
#         for panel in panels:
#             desc, dial = panel  # Unpack tuple
#             img_path = generate_image(desc, dial)
#             results.append({
#                 "description": desc,
#                 "dialogue": dial,
#                 "image": img_path
#             })

#         return {"panels": results}

#     except Exception as e:
#         return JSONResponse(status_code=500, content={"error": str(e)})

# # @app.post("/generate-comic")
# # async def generate_comic(request: Request):
# #     data = await request.json()
# #     text = data.get("text")
# #     panel_count = data.get("panel_count", 4)

# #     if not text:
# #         return JSONResponse(status_code=400, content={"error": "Missing 'text' field"})

# #     # Step 1: Generate scenes + dialogue
# #     panels = generate_storyboard(text, panel_count)

# #     # Step 2: Generate image for each panel
# #     result = []
# #     for panel in panels:
# #         description = panel["description"]
# #         dialogue = panel["dialogue"]
# #         img_path = generate_image(description, dialogue)
# #         result.append({
# #             "description": description,
# #             "dialogue": dialogue,
# #             "image": img_path
# #         })

#     return {"panels": result}

# @app.post("/generate-strip")
# async def generate_strip(request: Request):
#     data = await request.json()
#     image_paths = data.get("images", [])  # Relative URLs like /static/...

#     images = [Image.open(os.path.join("static", os.path.basename(p))) for p in image_paths]
#     widths, heights = zip(*(img.size for img in images))

#     total_width = sum(widths)
#     max_height = max(heights)
#     strip = Image.new('RGB', (total_width, max_height), color=(255, 255, 255))

#     x_offset = 0
#     for img in images:
#         strip.paste(img, (x_offset, 0))
#         x_offset += img.width

#     filename = f"strip_{uuid.uuid4().hex[:8]}.png"
#     path = os.path.join("static", filename)
#     strip.save(path)
#     return {"strip": f"/static/{filename}"}
