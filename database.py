import sqlite3


DB_PATH = "agent.db"


def init_database():
    with sqlite3.connect(DB_PATH) as connection:
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS memories (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                key TEXT UNIQUE NOT NULL,
                value TEXT NOT NULL
            )
            """
        )


def save_memory(key: str, value: str):
    with sqlite3.connect(DB_PATH) as connection:
        cursor = connection.execute(
            """
            INSERT INTO memories (key, value)
            VALUES (?, ?)
            ON CONFLICT(key) DO NOTHING
            """,
            (key, value),
        )

    return cursor.rowcount > 0


def load_memories():
    with sqlite3.connect(DB_PATH) as connection:
        rows = connection.execute(
            """
            SELECT key, value
            FROM memories
            ORDER BY id
            """
        ).fetchall()

    return {
        key: value
        for key, value in rows
    }


def update_memory(key: str, value: str):
    with sqlite3.connect(DB_PATH) as connection:
        cursor = connection.execute(
            """
            UPDATE memories
            SET value = ?
            WHERE key = ?
            """,
            (value, key),
        )

    return cursor.rowcount > 0


def delete_memory(key: str):
    with sqlite3.connect(DB_PATH) as connection:
        cursor = connection.execute(
            """
            DELETE FROM memories
            WHERE key = ?
            """,
            (key,),
        )

    return cursor.rowcount > 0