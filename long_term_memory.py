from database import (
    init_database,
    load_memories as db_load_memories,
    save_memory as db_save_memory,
    update_memory as db_update_memory,
    delete_memory as db_delete_memory,
)


init_database()


def load_long_term_memory() -> dict:
    return db_load_memories()


def save_long_term_memory(memory: dict) -> None:
    current_memory = db_load_memories()

    # Delete memories that are no longer present.
    for key in current_memory:
        if key not in memory:
            db_delete_memory(key)

    # Insert new memories or update existing ones.
    for key, value in memory.items():
        if key in current_memory:
            if current_memory[key] != value:
                db_update_memory(key, value)
        else:
            db_save_memory(key, value)


def save_memory(key: str, value: str) -> str:
    saved = db_save_memory(key, value)

    if not saved:
        return f"Memory key '{key}' already exists."

    return f"Saved {key} = {value}"


def update_memory(key: str, value: str) -> str:
    memory = db_load_memories()

    if key not in memory:
        return f"Memory key '{key}' does not exist."

    old_value = memory[key]

    db_update_memory(key, value)

    return f"Updated {key} from {old_value} to {value}"


def delete_memory(key: str) -> str:
    deleted = db_delete_memory(key)

    if not deleted:
        return f"Memory key '{key}' does not exist."

    return f"Deleted memory {key}"