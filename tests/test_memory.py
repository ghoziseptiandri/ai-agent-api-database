import database

from long_term_memory import (
    load_long_term_memory,
    save_memory,
    update_memory,
    delete_memory,
)


def setup_function():
    database.DB_PATH = "test_agent.db"
    database.init_database()


def teardown_function():
    import os

    if os.path.exists("test_agent.db"):
        os.remove("test_agent.db")


def test_save_memory():
    result = save_memory(
        "favorite_number",
        "11",
    )

    assert result == "Saved favorite_number = 11"

    memory = load_long_term_memory()

    assert memory == {
        "favorite_number": "11"
    }


def test_update_memory():
    save_memory(
        "favorite_number",
        "11",
    )

    result = update_memory(
        "favorite_number",
        "13",
    )

    assert result == "Updated favorite_number from 11 to 13"

    memory = load_long_term_memory()

    assert memory == {
        "favorite_number": "13"
    }


def test_delete_memory():
    save_memory(
        "favorite_number",
        "11",
    )

    result = delete_memory(
        "favorite_number"
    )

    assert result == "Deleted memory favorite_number"

    assert load_long_term_memory() == {}


def test_save_duplicate_memory():
    save_memory(
        "favorite_number",
        "11",
    )

    result = save_memory(
        "favorite_number",
        "13",
    )

    assert result == (
        "Memory key 'favorite_number' already exists."
    )

    assert load_long_term_memory() == {
        "favorite_number": "11"
    }


def test_update_missing_memory():
    result = update_memory(
        "favorite_number",
        "13",
    )

    assert result == (
        "Memory key 'favorite_number' does not exist."
    )


def test_delete_missing_memory():
    result = delete_memory(
        "favorite_number"
    )

    assert result == (
        "Memory key 'favorite_number' does not exist."
    )