import sqlite3

import database


def setup_function():
    database.DB_PATH = "test_agent.db"
    database.init_database()


def teardown_function():
    import os

    if os.path.exists("test_agent.db"):
        os.remove("test_agent.db")


def test_save_and_load_memory():
    database.save_memory("favorite_number", "7")

    memories = database.load_memories()

    assert memories == {
        "favorite_number": "7"
    }


def test_update_memory():
    database.save_memory("favorite_number", "7")

    updated = database.update_memory(
        "favorite_number",
        "9",
    )

    assert updated is True
    assert database.load_memories() == {
        "favorite_number": "9"
    }


def test_update_missing_memory():
    updated = database.update_memory(
        "unknown_key",
        "123",
    )

    assert updated is False


def test_delete_memory():
    database.save_memory("favorite_number", "7")

    deleted = database.delete_memory(
        "favorite_number"
    )

    assert deleted is True
    assert database.load_memories() == {}


def test_delete_missing_memory():
    deleted = database.delete_memory(
        "unknown_key"
    )

    assert deleted is False