import json
from datetime import datetime
from pathlib import Path

LOG_FILE = Path("agent.jsonl")


def log(event: str, data: dict | None = None) -> None:
    record = {
        "timestamp": datetime.now().isoformat(),
        "event": event,
        "data": data or {},
    }

    #print(record)

    with open(LOG_FILE, "a") as file:
        file.write(json.dumps(record) + "\n")