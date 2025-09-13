# core/ethics.py

def evaluate_action(action: str) -> bool:
    prohibited_keywords = [
        "harm humans",
        "weapon",
        "steal data",
        "illegal experiment",
        "self-replication",
        "bioweapon",
        "nuclear launch",
        "kill"
    ]
    action_lower = action.lower()
    for rule in prohibited_keywords:
        if rule in action_lower:
            return False
    return True
