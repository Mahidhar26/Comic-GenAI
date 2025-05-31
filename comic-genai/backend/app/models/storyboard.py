from pydantic import BaseModel
from typing import List

class Panel(BaseModel):
    id: int
    scene: str
    dialogue: str

class Storyboard(BaseModel):
    panels: List[Panel]
