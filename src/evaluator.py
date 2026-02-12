


EVALUATION_PATH = "./src/data/evaluation.json"

import json
import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

def evaluate_answer(session_json, resume_json):
    client = Groq(api_key=os.getenv("GROQ_API_KEY"))

    prompt = f"""
You are an interview answer evaluator.

ONLY analyze the answer. Do NOT teach or ask questions.
Analyze the quality of evaluation score based on the evaluation.

Interview Question:
{session_json["question"]}

Candidate Answer:
{session_json["answer"]}

Resume Context:
{json.dumps(resume_json, indent=2)}

Return ONLY JSON:

{{
  "evaluation_score": 0,
  "understood_concepts": [],
  "missing_concepts": [],
  "issues": [],
  "summary": ""
}}
"""
#   "correctness": 0.0,
#   "depth": 0.0,
#   "clarity": 0.0,

    response = client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=[
            {"role": "system", "content": "You evaluate answers objectively."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.2,
        max_tokens=600,
        response_format={"type": "json_object"}
    )

    return json.loads(response.choices[0].message.content)





# if __name__=="__main__":
    

#     with open("./src/data/resume.json","r") as f:
#         resume_json = json.load(f)

#     with open("./src/data/question.json","r") as f:
#         question_json = json.load(f)
    
#     evaluation = evaluate_answer(question_json, resume_json, level="B")
#     print(evaluation)
#     evaluation_json = json.loads(evaluation)

#     with open(EVALUATION_PATH, "w", encoding="utf-8") as f:
#         json.dump(evaluation_json, f, indent=2)
