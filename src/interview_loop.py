import json
from groq import Groq
import os
from dotenv import load_dotenv

from src.interviewer import generate_question
from src.evaluator import evaluate_answer
from src.strategy import decide_next_action

from src.session_memory import load_session, add_turn, end_session
from src.knowledge_memory import load_knowledge

load_dotenv()

MAX_QUESTIONS = 10

def run_interview(resume_json):
    client = Groq(api_key=os.getenv("GROQ_API_KEY"))

    session = load_session()
    knowledge = load_knowledge()

    question_count = 0
    followup_count = 0
    asked_questions = []

    while question_count < MAX_QUESTIONS:

        question = generate_question(client, resume_json, asked_questions)
        asked_questions.append(question)

        session["current_topic"] = "general"

        print(question)

        answer = input("\nYOUR ANSWER:\n> ")

        session_json = {
            "question": question,
            "answer": answer
        }

        evaluation = evaluate_answer(session_json, resume_json)
        print(evaluation)
        # evaluation = json.loads(evaluation)

        decision = decide_next_action(
            evaluation,
            session,
            knowledge,
            followup_count
        )

        print("\nSTRATEGY:", decision["action"])

        add_turn(
            session,
            question,
            decision.get("topic"),
            answer,
            evaluation
        )

        if decision["action"] == "drill":
            followup_count += 1
            print("\nFOLLOW-UP NEEDED...")
            continue

        if decision["action"] == "probe":
            followup_count += 1
            print("\nPROBING DEEPER...")
            continue

        followup_count = 0
        question_count += 1

    end_session(session)
    print("\nInterview finished.")