AUTO = "auto"
APPROVAL_REQUIRED = "approval_required"


TOOL_PERMISSIONS = {
    "calculate": AUTO,
    "get_current_time": AUTO,
    "get_weather": AUTO,
    "read_file": AUTO,

    "save_memory": APPROVAL_REQUIRED,
    "update_memory": APPROVAL_REQUIRED,
    "delete_memory": APPROVAL_REQUIRED,
}


def get_tool_permission(tool_name: str) -> str:
    return TOOL_PERMISSIONS.get(tool_name, APPROVAL_REQUIRED)


def requires_approval(tool_name: str) -> bool:
    return get_tool_permission(tool_name) == APPROVAL_REQUIRED