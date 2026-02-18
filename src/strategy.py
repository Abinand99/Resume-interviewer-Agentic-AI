from typing import Dict

def decide_next_action(
    evaluation: Dict,
    session_state: Dict,
    followup_count: int
) -> Dict:
    

    score = evaluation.get("evaluation_score", 0)
    missing = evaluation.get("missing_concepts", [])
    topic = missing[0] if missing else session_state.get("current_topic", "general")

    if score <=1:
        return {"action": "move_on", "topic": None, "reason": "Dont Know or Zero understanding"}
        

    elif score < 4:
        if followup_count < 2:
            return {"action": "drill", "topic": topic, "reason": "Weak answer"}
        return {"action": "move_on", "topic": None, "reason": "Too many followups"}

    elif score < 8:
        if followup_count < 1:
            return {"action": "probe", "topic": topic, "reason": "Partial understanding"}
        return {"action": "move_on", "topic": None, "reason": "Probe done"}
    else:
        return {"action": "move_on", "topic": None, "reason": "Strong answer"}