# import json
# from src.session_manager import load_session, save_session, add_interaction
# from src.interviewer import generate_question
# from src.evaluator import evaluate_answer

# with open("./src/data/resume.json", "r") as f:
#     resume_json = json.load(f)

# session = load_session()

# with open("./src/data/question.json","r") as f:
#     question_json = json.load(f)

# evaluation_raw = evaluate_answer(
#     session_json=question_json,
#     resume_json=resume_json,
#     level=session["difficulty_mode"]
# )

# try:
#     evaluation = json.loads(evaluation_raw)
# except json.JSONDecodeError:
#     print("\n Evaluation parsing failed")
#     print(evaluation_raw)

# print("\n EVALUATION RESULT")
# print("Score:", evaluation.get("score"))
# print("\nStrengths:", evaluation.get("strengths"))
# print("\nMissing Concepts:", evaluation.get("missing_concepts"))
# print("\nCritique:", evaluation.get("critique"))
# print("\nFollow-up Question:", evaluation.get("follow_up_question"))

# add_interaction(session, question_json["question"], question_json["answer"], evaluation)
# save_session(session)


# if __name__ == "__main__":
#     main()

import json
from src.interview_loop import run_interview

with open("./src/data/resume.json", "r") as f:
    resume_json = json.load(f)

run_interview(resume_json)