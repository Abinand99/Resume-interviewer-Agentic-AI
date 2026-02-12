import json
import os
from datetime import datetime
from typing import Dict

KNOWLEDGE_PATH = "./src/data/knowledge_memory.json"

def load_knowledge() -> Dict:
    if not os.path.exists(KNOWLEDGE_PATH):
        return {}

    with open(KNOWLEDGE_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

def save_knowledge(knowledge: Dict):
    os.makedirs(os.path.dirname(KNOWLEDGE_PATH), exist_ok=True)
    with open(KNOWLEDGE_PATH, "w", encoding="utf-8") as f:
        json.dump(knowledge, f, indent=2)

def update_topic_knowledge(
        knowledge: Dict,
        topic: str,
        evaluation: Dict
):
    if not topic:
        return
    
    score = evaluation.get("overall_score",0)

    if topic not in knowledge:
        knowledge[topic] = {
            "strength": 0.5,
            "fail_count": 0,
            "success_count": 0,
            "last_tested": None
        }
    topic_data = knowledge[topic]

    if score < 5:
        topic_data["fail_count"] += 1
        topic_data["strength"] = max(0.0, topic_data["strength"]- 0.1)
    else:
        topic_data["success_count"] += 1
        topic_data["strength"] = min(1.0, topic_data["strength"] + 0.1)

    topic_data["last_tested"] = datetime.now().isoformat()

    save_knowledge(knowledge)