import json
import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

def generate_progress_summary(knowledge_memory):
    client = Groq(api_key=os.getenv("GROQ_API_KEY"))

    prompt = f"""
You are an AI interview coach.

Analyze the user's interview history stored below and summarize their progress.

Knowledge Memory:
{json.dumps(knowledge_memory, indent=2)}

Return JSON:

{{
  "progress_summary": "",
  "trend": "",
  "focus_areas": []
}}
"""

    response = client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=[
            {"role": "system", "content": "You analyze interview progress."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.3,
        response_format={"type": "json_object"},
        max_tokens=1200
    )

    return json.loads(response.choices[0].message.content)
