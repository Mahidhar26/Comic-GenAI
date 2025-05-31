from pydantic import BaseModel, Field

class StoryRequest(BaseModel):
    text: str = Field(..., max_length=1000)
    panel_count: int = Field(ge=1, le=6, default=4)