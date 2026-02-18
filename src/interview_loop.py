import json
from groq import Groq
import os
from dotenv import load_dotenv

from src.interviewer import generate_question,generate_followup_question
from src.evaluator import evaluate_answer
from src.strategy import decide_next_action

from src.session_memory import load_session, add_turn, end_session
from src.knowledge_memory import add_session_summary,load_knowledge
from src.summary_agent import generate_interview_summary
from src.progress_analyzer import generate_progress_summary

load_dotenv()

MAX_QUESTIONS = 10

def run_interview(resume_json):
    client = Groq(api_key=os.getenv("GROQ_API_KEY"))

    session = load_session()

    question_count = 0
    followup_count = 0
    asked_questions = []

    while question_count < MAX_QUESTIONS:

        followup_count = 0

        question = generate_question(
            client,
            resume_json,
            asked_questions
        )
        asked_questions.append(question)

        session["current_topic"] = "general"

        print("\nINTERVIEWER:", question)

        answer = input("\nYOUR ANSWER:\n> ")

        session_json = {"question": question, "answer": answer}

        evaluation = evaluate_answer(session_json, resume_json)

        add_turn(
            session,
            question,
            session["current_topic"],
            answer,
            evaluation
        ) 

        decision = decide_next_action(evaluation, 
                                      session,
                                      followup_count
                                      )
        followup_chain = [{"q": question, "a": answer}]

        while decision["action"] in ["drill","probe"]:

            followup_count +=1

            followup_q = generate_followup_question(
                client,
                resume_json,
                followup_chain,
                evaluation.get("missing_concepts", []),
                mode=decision["action"]
            )

            print("\nFOLLOW-UP:", followup_q)

            followup_answer = input("\nYOUR ANSWER:\n> ")

            followup_chain.append({"q": followup_q, "a": followup_answer})

            session_json = {"question": followup_q, "answer": followup_answer}
            evaluation = evaluate_answer(session_json, resume_json)

            add_turn(session, followup_q, "general", followup_answer, evaluation)

            decision = decide_next_action(evaluation, session, knowledge, followup_count)
        
        question_count += 1
    end_session(session)

    summary = generate_interview_summary(session)
    
    add_session_summary(summary)

    print("\nINTERVIEW SUMMARY")
    print(json.dumps(summary, indent=2))

    knowledge = load_knowledge()
    progress_summary = generate_progress_summary(knowledge)


    print("\nPROGRESS SUMMARY")
    print(json.dumps(progress_summary, indent=2))
