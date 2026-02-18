import json
import os
from groq import Groq
from dotenv import load_dotenv
# from src.data import session_memory

load_dotenv()

# with open("src/data/session_memory.json",'r',encoding="utf-8") as f:
#     session = json.load(f)

def generate_interview_summary(session):
    client = Groq(api_key=os.getenv("GROQ_API_KEY"))

    turns = session.get("turns",[])

    prompt = f"""
You are an interview feedback assistant.

Analyze the interview session below and generate feedback.

Interview Turns:
{json.dumps(turns, indent=2)}

Provide feedback in JSON format:

{{
  "strengths": [],
  "weak_areas": [],
  "knowledge_gaps": [],
  "communication_feedback": "",
  "overall_performance": "",
  "improvement_advice": []
}}

Rules:
- Be constructive
- Be specific
- Identify repeated weak topics
- Focus on technical clarity and depth
- Do not invent topics not present in session
"""
    response = client.chat.completions.create(
        model= "openai/gpt-oss-120b",
        messages=[
            {"role": "system", "content": "You analyze interview sessions."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.2,
        max_tokens=1200,
        response_format={"type": "json_object"}
    )

    return json.loads(response.choices[0].message.content)




