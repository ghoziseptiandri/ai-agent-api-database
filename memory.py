import json
from pathlib import Path

MEMORY_FILE = Path("memory.json")


def load_memory() -> list:
    if not MEMORY_FILE.exists():
        return []

    with open(MEMORY_FILE, "r") as file:
        return json.load(file)


def save_memory(memory: list) -> None:
    with open(MEMORY_FILE, "w") as file:
        json.dump(memory, file, indent=2)