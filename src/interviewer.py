
import json
# from huggingface_hub import InferenceClient
import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()


def generate_question(model, resume_json, asked_questions):
    prompt = f"""
You are a senior technical interviewer.

Based ONLY on the resume data below, ask ONE interview question.

IMPORTANT:
These questions have ALREADY been asked:
{json.dumps(asked_questions, indent=2)}

Rules:
- Ask like a real interviewer
- Focus on projects, skills, or experience
- Ask for depth, reasoning, or design choices
- Ask only ONE question
- Do NOT explain anything
- Do NOT answer the question
- STRICTLY avoid repeating or rephrasing previously asked questions

Resume data:
{json.dumps(resume_json, indent=2)}
"""

    response = model.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=[
            {"role": "system", "content": "You are a strict technical interviewer."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.4,
        max_completion_tokens=400
    )

    # return response.choices[0].message.content.strip()
    question = response.choices[0].message.content.strip()

    if len(question) < 20 or "?" not in question:
        return generate_question(model, resume_json, asked_questions)

    return question

def generate_followup_question(
        model,
        resume_json,
        followup_chain,
        missing_concepts,
        mode ="probe"
):
    prompt = f"""
You are a technical interviewer asking a follow-up question.

Conversation so far:
{json.dumps(followup_chain, indent=2)}

Missing Concepts:
{missing_concepts}

Follow-up mode:
{mode}

Instructions:
- Ask ONE follow-up question
- If mode is "drill", ask deeper technical reasoning
- If mode is "probe", ask clarification question
- Focus on missing concepts
- Do not explain anything
- Do not ask multiple questions
- Keep it natural like an interviewer

Resume context:
{resume_json}
"""
    response = model.chat.completions.create(
        model = "openai/gpt-oss-120b",
        messages = [
            {"role":"system","content": "You are a strict interviewer."},
            {"role": "user", "content": prompt}
        ],
        temperature = 0.4,
        max_completion_tokens =300
    )
    # return response.choices[0].message.content.strip()

    question = response.choices[0].message.content.strip()
    
    if len(question) < 20 or "?" not in question:
        return generate_question(model, resume_json, asked_questions)

    return question

def load_question(path_question):
    if not os.path.exists(path_question):
        return {"asked_questions": []}

    with open(path_question, "r", encoding="utf-8") as f:
        return json.load(f)

def save_question(state):
    with open(STATE_PATH, "w", encoding="utf-8") as f:
        json.dump(state, f, indent=2)

def add_question(state, question):
    state["asked_questions"].append(question)
    save_question(state)

def load_resume_json(path_resume):
    with open(path_resume, "r") as f:
        return json.load(f)



def save_session(question, answer, path_session,evaluation=None):
    session = {
        "question": question,
        "answer": answer
    }
    with open(path_session, "w", encoding="utf-8") as f:
        json.dump(session, f, indent=2)



if __name__ == "__main__":

    # model = InferenceClient(
    #     model="Qwen/Qwen2.5-14B-Instruct",
    #     token=os.getenv("HUGGINGFACEHUB_API_TOKEN")
    # )
    SESSION_PATH = "./src/data/question.json"
    STATE_PATH = "./src/data/question_state.json"
    RESUME_PATH = "./src/data/resume.json"

    model = Groq(api_key=os.getenv("GROQ_API_KEY"))

    resume_json = load_resume_json(RESUME_PATH)

    question_state = load_question()
    asked_questions = question_state["asked_questions"]
    
    question = generate_question(model, 
                                 resume_json,
                                 asked_questions
                                 )
    print("\nINTERVIEW QUESTION:\n", question)

    print("\nYOUR ANSWER (press Enter when done):\n")
    answer = input("\nYOUR ANSWER:\n> ")
    save_session(question, answer,SESSION_PATH)
    

