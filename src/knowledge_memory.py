import json
import os
from datetime import datetime
from typing import Dict

KNOWLEDGE_PATH = "./src/data/knowledge_memory.json"

def load_knowledge() -> Dict:
    if not os.path.exists(KNOWLEDGE_PATH):
        return {
            "sessions": [],
            "total_sessions": 0
        }

    with open(KNOWLEDGE_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

def save_knowledge(knowledge: Dict):
    os.makedirs(os.path.dirname(KNOWLEDGE_PATH), exist_ok=True)
    with open(KNOWLEDGE_PATH, "w", encoding="utf-8") as f:
        json.dump(knowledge, f, indent=2)

def add_session_summary(summary: Dict):
    knowledge = load_knowledge()

    session_record = {
        "date": datetime.now().isoformat(),
        "overall_performance": summary.get("overall_performance"),
        "strengths": summary.get("strengths", []),
        "weak_areas": summary.get("weak_areas", []),
        "knowledge_gaps": summary.get("knowledge_gaps", []),
        "improvement_advice": summary.get("improvement_advice",[])
    }

    knowledge["sessions"].append(session_record)
    knowledge["total_sessions"] += 1

    save_knowledge(knowledge)