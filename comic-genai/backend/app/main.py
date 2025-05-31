from fastapi import FastAPI, HTTPException
from app.models.request import StoryRequest
from app.models.storyboard import Storyboard
from app.services.storyboard import generate_storyboard
from fastapi.middleware.cors import CORSMiddleware
from fastapi import Body
from app.services.imagegen import generate_image
from fastapi.staticfiles import StaticFiles
from fastapi import FastAPI, Request

app = FastAPI(title="ComicGen API")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.mount("/static", StaticFiles(directory="."), name="static")

@app.post("/storyboard", response_model=Storyboard)
async def storyboard(req: StoryRequest):
    print("🔍 Received request:", req)
    try:
        return generate_storyboard(req.text, req.panel_count)
    except Exception as exc:
        print("Exception:", exc)
        raise HTTPException(status_code=400, detail=str(exc))


def generate_image(prompt: str, dialogue: str = "", position: str = "bottom-left") -> str:
    image = pipe(prompt).images[0]
    if dialogue:
        image = overlay_dialogue(image, dialogue, position)
    
    filename = f"panel_{uuid.uuid4().hex[:8]}.png"
    path = os.path.join("static", filename)
    image.save(path)
    return f"/static/{filename}"

@app.post("/generate-comic")
async def generate_comic(request: Request):
    data = await request.json()
    text = data.get("text")
    panel_count = data.get("panel_count", 4)

    if not text:
        return JSONResponse(status_code=400, content={"error": "Missing 'text' field"})

    # Step 1: Generate scenes + dialogue
    panels = generate_storyboard(text, panel_count)

    # Step 2: Generate image for each panel
    result = []
    for panel in panels:
        description = panel["description"]
        dialogue = panel["dialogue"]
        img_path = generate_image(description, dialogue)
        result.append({
            "description": description,
            "dialogue": dialogue,
            "image": img_path
        })

    return {"panels": result}

@app.post("/generate-strip")
async def generate_strip(request: Request):
    data = await request.json()
    image_paths = data.get("images", [])  # Relative URLs like /static/...

    images = [Image.open(os.path.join("static", os.path.basename(p))) for p in image_paths]
    widths, heights = zip(*(img.size for img in images))

    total_width = sum(widths)
    max_height = max(heights)
    strip = Image.new('RGB', (total_width, max_height), color=(255, 255, 255))

    x_offset = 0
    for img in images:
        strip.paste(img, (x_offset, 0))
        x_offset += img.width

    filename = f"strip_{uuid.uuid4().hex[:8]}.png"
    path = os.path.join("static", filename)
    strip.save(path)
    return {"strip": f"/static/{filename}"}