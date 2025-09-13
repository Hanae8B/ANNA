import os
import datetime

LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)

def log_action(action: str, response: str, confirmed: bool, module: str):
    timestamp = datetime.datetime.now().isoformat()
    log_file = os.path.join(LOG_DIR, f"{module}_log.txt")
    with open(log_file, "a", encoding="utf-8") as f:
        f.write(f"{timestamp} | ACTION: {action} | CONFIRMED: {confirmed} | RESPONSE: {response}\n")
