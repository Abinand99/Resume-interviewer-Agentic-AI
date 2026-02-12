import json
import os
from datetime import datetime

from typing import Dict, Optional

SESSION_PATH = "./src/data/session_memory.json"

def create_new_session()->Dict:
    return {
        "session_id": f"session_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
        "current_topic": None,
        "turns": [],
        "ended": False
    }

def load_session()->Dict:
    if not os.path.exists(SESSION_PATH):
        return create_new_session()
    
    with open(SESSION_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

def save_session(session: Dict):
    os.makedirs(os.path.dirname(SESSION_PATH),exist_ok=True)
    with open(SESSION_PATH, "w", encoding="utf-8") as f:
        json.dump(session, f , indent=2)

def add_turn(
       session:Dict,
       question:str,
       topic:str,
       answer:str,
       evaluation: Dict 
):
    turn = {
       "question":question,
       "topic":topic,
       "answer":answer,
       "evaluation":{
           "evaluation_score":evaluation.get("evaluation_score",0)
           } 
    }
    session["turns"].append(turn)
    session["current_topic"] = topic
    save_session(session)

def end_session(session:Dict):
    session["ended"] = True
    save_session(session)
