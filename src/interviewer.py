
import json
from huggingface_hub import InferenceClient
import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()


def generate_question(model , resume_json):
    prompt = """
You are a senior technical interviewer.

Based ONLY on the resume data below, ask ONE interview question.

Rules:
- Ask like a real interviewer.
- Focus on projects, skills, or experience.
- Ask for depth, reasoning, or design choices.
- Ask only ONE question.
- Do NOT explain anything.
- Do NOT answer the question.

Resume data:
{json.dumps(resume_json, indent=2)}
"""
    # response = model.chat.completions.create(
    #     messages=[{"role": "user", "content": prompt}],
    #     max_tokens=300,
    #     temperature=0.5
    # )
    response = model.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=[
            {
                "role": "system",
                "content": "You are a strict technical interviewer."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.4,
        max_completion_tokens=500
    )
    return response.choices[0].message.content.strip()


if __name__ == "__main__":

    # model = InferenceClient(
    #     model="Qwen/Qwen2.5-14B-Instruct",
    #     token=os.getenv("HUGGINGFACEHUB_API_TOKEN")
    # )
    model = Groq(api_key=os.getenv("GROQ_API_KEY"))

    with open("./src/data/resume.json", "r") as f:
        resume_json = json.load(f)
    
    question = generate_question(model, resume_json)
    print("\nINTERVIEW QUESTION:\n", question)