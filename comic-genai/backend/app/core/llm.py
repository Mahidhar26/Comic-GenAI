import os
import json
from jinja2 import Template
from openai import OpenAI

from .config import get_settings

settings = get_settings()
client = OpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1"
)

TEMPLATE = Template(open("prompts/storyboard.jinja").read())

def gpt_storyboard(user_text: str, panel_count: int = 4) -> dict:
    prompt = TEMPLATE.render(user_text=user_text.strip(), panel_count=panel_count)
    resp = client.chat.completions.create(
        model="llama3-70b-8192",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
        max_tokens=700,
    )
    content = resp.choices[0].message.content
    first_brace = content.find('{')
    return json.loads(content[first_brace:])