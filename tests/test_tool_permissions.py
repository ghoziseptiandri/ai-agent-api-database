from tools.tool_permissions import (
    AUTO,
    APPROVAL_REQUIRED,
    get_tool_permission,
    requires_approval,
)


def test_safe_tool_is_auto():
    assert get_tool_permission("get_weather") == AUTO


def test_sensitive_tool_requires_approval():
    assert get_tool_permission("delete_memory") == APPROVAL_REQUIRED


def test_unknown_tool_requires_approval():
    assert get_tool_permission("unknown_tool") == APPROVAL_REQUIRED

def test_requires_approval():
    assert requires_approval("delete_memory") is True
    assert requires_approval("get_weather") is False