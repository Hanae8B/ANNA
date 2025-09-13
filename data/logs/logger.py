# core/logger.py
import os
import datetime
import json

LOG_DIR = r"C:\ANNA\data/logs"
os.makedirs(LOG_DIR, exist_ok=True)
LOG_FILE = os.path.join(LOG_DIR, "anna_log.json")

def log_action(user_query: str, module: str, response: str, confirmed: bool):
    """
    Logs each user interaction with ANNA.
    """
    log_entry = {
        "timestamp": datetime.datetime.now().isoformat(),
        "query": user_query,
        "module": module,
        "response": response,
        "confirmed": confirmed
    }

    # Read existing logs
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, "r", encoding="utf-8") as f:
            logs = json.load(f)
    else:
        logs = []

    # Append new log
    logs.append(log_entry)

    # Save back
    with open(LOG_FILE, "w", encoding="utf-8") as f:
        json.dump(logs, f, indent=4)

def read_logs():
    """Return all logged actions."""
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []
