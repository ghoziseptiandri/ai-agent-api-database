from tools.registry import TOOL_FUNCTIONS


def test_calculator_registered():
    assert "calculate" in TOOL_FUNCTIONS


def test_time_tool_registered():
    assert "get_current_time" in TOOL_FUNCTIONS


def test_save_memory_registered():
    assert "save_memory" in TOOL_FUNCTIONS