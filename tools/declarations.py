from google.genai import types

calculator_tool = types.Tool(
    function_declarations=[
        types.FunctionDeclaration(
            name="calculate",
            description="Perform a mathematical calculation.",
            parameters=types.Schema(
                type="OBJECT",
                properties={
                    "a": types.Schema(type="NUMBER"),
                    "b": types.Schema(type="NUMBER"),
                    "operation": types.Schema(
                        type="STRING",
                        description="add, subtract, multiply, or divide"
                    ),
                },
                required=["a", "b", "operation"],
            ),
        )
    ]
)

time_tool = types.Tool(
    function_declarations=[
        types.FunctionDeclaration(
            name="get_current_time",
            description="Get the current local date and time.",
            parameters=types.Schema(
                type="OBJECT",
                properties={},
            ),
        )
    ]
)

memory_tool = types.Tool(
    function_declarations=[
        types.FunctionDeclaration(
            name="save_memory",
            description=(
                "Save an important long-term fact about the user. "
                "Use this for stable preferences or information "
                "that may be useful in future conversations."
            ),
            parameters=types.Schema(
                type="OBJECT",
                properties={
                    "key": types.Schema(
                        type="STRING",
                        description=(
                            "A short descriptive key, "
                            "for example favorite_number."
                        ),
                    ),
                    "value": types.Schema(
                        type="STRING",
                        description="The fact to remember.",
                    ),
                },
                required=["key", "value"],
            ),
        )
    ]
)
update_memory_tool = types.Tool(
    function_declarations=[
        types.FunctionDeclaration(
            name="update_memory",
            description="Update an existing long-term memory.",
            parameters=types.Schema(
                type="OBJECT",
                properties={
                    "key": types.Schema(
                        type="STRING",
                        description="The existing memory key."
                    ),
                    "value": types.Schema(
                        type="STRING",
                        description="The new value."
                    ),
                },
                required=["key", "value"],
            ),
        )
    ]
)

delete_memory_tool = types.Tool(
    function_declarations=[
        types.FunctionDeclaration(
            name="delete_memory",
            description="Delete a long-term memory that the user wants forgotten.",
            parameters=types.Schema(
                type="OBJECT",
                properties={
                    "key": types.Schema(
                        type="STRING",
                        description="The memory key to delete."
                    ),
                },
                required=["key"],
            ),
        )
    ]
)

file_reader_tool = types.Tool(
    function_declarations=[
        types.FunctionDeclaration(
            name="read_file",
            description=(
                "Read the contents of a local text file."
            ),
            parameters=types.Schema(
                type="OBJECT",
                properties={
                    "file_path": types.Schema(
                        type="STRING",
                        description=(
                            "Path of the file to read."
                        ),
                    ),
                },
                required=["file_path"],
            ),
        )
    ]
)

weather_tool = types.Tool(
    function_declarations=[
        types.FunctionDeclaration(
            name="get_weather",
            description="Get the current weather for a city.",
            parameters=types.Schema(
                type="OBJECT",
                properties={
                    "city": types.Schema(
                        type="STRING",
                        description="The city name, for example Jakarta or Tokyo."
                    )
                },
                required=["city"],
            ),
        )
    ]
)

GEMINI_TOOLS = [
    calculator_tool,
    time_tool,
    memory_tool,
    update_memory_tool,
    delete_memory_tool,
    file_reader_tool,
    weather_tool
]