from app.core.llm import gpt_storyboard
from app.models.storyboard import Storyboard

def generate_storyboard(user_text: str, panel_count: int = 4) -> Storyboard:
    raw = gpt_storyboard(user_text, panel_count)
    return Storyboard.model_validate(raw)
