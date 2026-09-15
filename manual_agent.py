from google.genai import types
from config import MAX_TOOL_LOOPS, MODEL_NAME, client
from tools.declarations import GEMINI_TOOLS
from logger import log
from prompts import SYSTEM_INSTRUCTION
from tools.registry import TOOL_FUNCTIONS

from tools.tool_permissions import (
    requires_approval
)

def run_agent(
    user_input: str,
    contents: list,
    memory_context: str = ""
) -> tuple[str, list]:

    if memory_context:
        contents.append(
            types.Content(
                role="user",
                parts=[
                    types.Part.from_text(text=memory_context)
                ]
            )
        )

    contents.append(
        types.Content(
            role="user",
            parts=[
                types.Part.from_text(text=user_input)
            ],
        )
    )

    log(
        "user_message",
        {
            "text": user_input
        }
    )

    # ... add user message etc.

    for loop_count in range(MAX_TOOL_LOOPS):
        log(
            "agent_loop",
            {
                "loop": loop_count + 1
            }
        )

        log("gemini_request_start")

        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=contents,
            config=types.GenerateContentConfig(
                tools=GEMINI_TOOLS,
                system_instruction=SYSTEM_INSTRUCTION,
            ),
        )

        # TOOL PATH
        if response.function_calls:
            # 1. Save Gemini's function-call turn
            contents.append(response.candidates[0].content)

            function_response_parts = []

            for function_call in response.function_calls:
                function_name = function_call.name
                function_args = dict(function_call.args)

                log(
                    "tool_requested",
                    {
                        "tool": function_name,
                        "arguments": function_args,
                    }
                )

                if requires_approval(function_name):
                    approval = input(
                        f"Approve {function_name} {function_args}? (y/n): "
                    ).strip().lower()

                    if approval not in {"y", "yes"}:
                        result = {
                            "approved": False,
                            "message": "User denied this tool call.",
                        }
                    else:
                        tool_function = TOOL_FUNCTIONS[function_name]
                        result = tool_function(**function_args)

                else:
                    tool_function = TOOL_FUNCTIONS[function_name]
                    result = tool_function(**function_args)

                function_response_parts.append(
                    types.Part.from_function_response(
                        name=function_name,
                        response={"result": result},
                    )
                )

            # 2. Send tool result back as the next turn
            contents.append(
                types.Content(
                    role="user",
                    parts=function_response_parts,
                )
            )

            continue

        # FINAL ANSWER PATH
        contents.append(
            response.candidates[0].content
        )

        log(
            "agent_response",
            {
                "text": response.text
            }
        )

        return response.text, contents

    # We only reach here if all loops were used
    log(
        "max_tool_loops_reached",
        {
            "limit": MAX_TOOL_LOOPS
        }
    )

    return (
        "The agent reached the maximum number of tool steps.",
        contents
    )