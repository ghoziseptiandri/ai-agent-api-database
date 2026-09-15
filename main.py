from google.genai import types
from config import MAX_MEMORY_ITEMS
from manual_agent import run_agent
from memory import load_memory, save_memory
from long_term_memory import load_long_term_memory

long_term_memory = load_long_term_memory()
memory_context = ""

if long_term_memory:
    memory_context = f"""
    Here are some long-term facts about the user:

    {long_term_memory}
    """

def main():
    print("Simple AI Agent")
    print("Type 'exit' or 'quit' to stop.")

    memory = load_memory()

    # Keep only the most recent conversations
    memory = memory[-MAX_MEMORY_ITEMS:]

    contents = []

    for item in memory:
        contents.append(
            types.Content(
                role="user",
                parts=[
                    types.Part.from_text(
                        text=item["user"]
                    )
                ],
            )
        )

        contents.append(
            types.Content(
                role="model",
                parts=[
                    types.Part.from_text(
                        text=item["agent"]
                    )
                ],
            )
        )

    while True:
        user_input = input("\nYou: ")

        if user_input.lower() in ["exit", "quit"]:
            print("Goodbye!")
            break

        answer, contents = run_agent(
            user_input,
            contents,
            memory_context
        )

        memory.append({
            "user": user_input,
            "agent": answer
        })

        print(f"\nAgent: {answer}")

        # Keep persistent memory limited too
        memory = memory[-MAX_MEMORY_ITEMS:]

        save_memory(memory)

if __name__ == "__main__":
    main()