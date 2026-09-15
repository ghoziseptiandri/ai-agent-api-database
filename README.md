# Basic AI Agent with Gemini + Python + SQL - #MakeItPublic Part 2

**Disclaimer: This project was built as a hands-on learning exercise. The code and structure evolved through experimentation, debugging, and conversations with ChatGPT.**

This is Part 2 of my AI agent learning project.

Part 1 builds the core agent foundations: Gemini chat, manual function calling, a tool registry, conversation and long-term memory, logging, testing, and the agent loop.

**Start with Part 1 for the initial setup and foundation:**

https://github.com/ghoziseptiandri/ai-agent-template

In Part 2, I extended that foundation with more realistic tools, safety controls, and SQLite-backed long-term memory.

> This is a learning project, not a production-ready agent yet.

## Phase 2 - Tools, Safety & Database Memory

This phase covers:

### Real-World Tools

- File Reading Tools
- External API Calls

### Safety & Control

- Human Approval
- Tool Permissions

### Database Memory

- SQLite
- Database-Backed Memory
- Migrating from JSON to SQLite

### Before Starting (Reminder Again!)

This project continues directly from Part 1. If you have not completed Part 1 yet, start here:

https://github.com/ghoziseptiandri/ai-agent-template

Part 1 already provides the core architecture used in this phase, including:

- Gemini API integration
- Manual function/tool calling
- Tool registry
- Agent loop
- Conversation history
- Long-term memory tools
- Logging
- Automated testing
- Configuration and prompts

Instead of rebuilding those pieces, Part 2 extends them.

Conceptually:

```text
Part 1
Core Agent Foundations
        ↓
Part 2
Real-World Tools
        ↓
Safety & Human Approval
        ↓
SQLite Database Memory
```

## What Changed in Part 2

The agent can now:

- Read local files through a tool
- Retrieve weather data from an external API
- Assign permissions to tools
- Require human approval before sensitive operations
- Automatically execute tools that do not require approval
- Return a denial result to Gemini when the user rejects a tool call
- Store long-term memory in SQLite
- Save, load, update, and delete database-backed memories
- Persist memory across application restarts
- Migrate existing JSON memory into SQLite
- Test the new tools, permissions, and database operations with `pytest`

## 1. File Reading Tools

The first addition was a tool that lets the agent read a local file.

This helped me understand that an AI agent does not automatically have access to files on my computer.

Instead, Gemini requests a tool and Python performs the actual file operation.

Conceptually:

```text
User
  ↓
Gemini
  ↓
Gemini requests read_file()
  ↓
Python opens the file
  ↓
File content
  ↓
Result goes back to Gemini
  ↓
Gemini answers
```

The important distinction is:

```text
Gemini
→ decides that file content is needed

Python tool
→ actually reads the file
```

This is also an early step toward understanding retrieval systems, because the model can receive information that exists outside its own context.

### File Reader Tool

The file-reading tool lives in:

```text
tools/file_reader.py
```

It is then registered with the other tools so Gemini can request it.

Conceptually:

```python
TOOL_FUNCTIONS = {
    "calculate": calculate,
    "get_current_time": get_current_time,
    "read_file": read_file,
}
```

The exact tool implementation can change, but the architecture stays simple:

```text
Gemini tool request
        ↓
Tool Registry
        ↓
read_file()
        ↓
Local file
```

### Testing the File Reader

I added automated tests for the file-reading behavior.

The tests cover cases such as:

- Reading an existing file
- Handling a missing file

Run the tests with:

```bash
python -m pytest tests/test_file_reader.py -v
```

## 2. External API Calls

After reading local files, I wanted the agent to retrieve real-world information from an external service.

I added a weather tool using the Open-Meteo API.

The tool does not require a separate weather API key.

The flow is:

```text
User asks about weather
        ↓
Gemini
        ↓
get_weather(city)
        ↓
Python sends HTTP request
        ↓
Open-Meteo API
        ↓
Weather data
        ↓
Python returns tool result
        ↓
Gemini answers
```

Again, Gemini is not directly making the HTTP request.

Gemini decides that `get_weather()` should be called. Python performs the network request and returns the result.

### Weather Tool

The weather tool lives in:

```text
tools/weather.py
```

It is registered alongside the existing tools:

```python
TOOL_FUNCTIONS = {
    "calculate": calculate,
    "get_current_time": get_current_time,
    "read_file": read_file,
    "get_weather": get_weather,
}
```

This showed me that tools can connect an agent to information outside the model:

```text
Agent
  ↓
Tool
  ↓
External Service
  ↓
Real-world data
```

### Testing External API Tools

External APIs introduce another testing problem: I do not want every automated test to depend on a live internet request.

Instead, the weather tests mock the network response.

This keeps the tests:

- Faster
- Predictable
- Independent from temporary API/network failures

Run:

```bash
python -m pytest tests/test_weather.py -v
```

## 3. Tool Permissions

Once the agent could interact with more tools, I needed to think about which operations should run automatically.

Not every tool has the same level of risk.

For example:

```text
calculate
→ reads/computes information

get_weather
→ retrieves information

save_memory
→ changes persistent data

delete_memory
→ deletes persistent data
```

So I added a simple permission layer.

The permission logic lives in:

```text
tools/tool_permissions.py
```

The model uses two permission states:

```python
AUTO = "auto"
APPROVAL_REQUIRED = "approval_required"
```

Conceptually, the permission table looks like:

```python
TOOL_PERMISSIONS = {
    "calculate": AUTO,
    "get_current_time": AUTO,
    "get_weather": AUTO,
    "read_file": AUTO,
    "save_memory": APPROVAL_REQUIRED,
    "update_memory": APPROVAL_REQUIRED,
    "delete_memory": APPROVAL_REQUIRED,
}
```

This means read-only or low-risk tools can execute automatically, while tools that modify persistent memory require confirmation.

### Fail-Safe Default

An important decision was what should happen if a tool is not listed in the permission table.

Instead of automatically allowing it, unknown tools require approval.

Conceptually:

```text
Known AUTO tool
      ↓
Run automatically

Known sensitive tool
      ↓
Ask for approval

Unknown tool
      ↓
Ask for approval
```

This gives the permission system a safer default.

## 4. Human Approval

Tool permissions tell the agent which tools require confirmation.

Human approval is the actual step where the program asks the user before executing one of those tools.

For example:

```text
You: Remember that my favorite drink is coffee.

Gemini requests:
save_memory(
    key="favorite_drink",
    value="coffee"
)

Approval required.

Approve? (y/n): y

Tool executes.
```

If the user approves:

```text
Gemini
  ↓
save_memory requested
  ↓
Permission check
  ↓
Approval required
  ↓
User: y
  ↓
Execute tool
```

If the user denies:

```text
Gemini
  ↓
save_memory requested
  ↓
Permission check
  ↓
Approval required
  ↓
User: n
  ↓
Do not execute tool
  ↓
Return denial result to Gemini
```

Returning a tool result even when the action is denied is important because Gemini still needs a response for the function call it requested.

### Why Approval Happens Outside Gemini

Gemini can request a tool, but the Python application controls whether that tool actually executes.

That separation looks like:

```text
Gemini
→ "I want to call delete_memory"

Python
→ checks tool permission

User
→ approves or denies

Python
→ executes only if allowed
```

This helped me understand that tool calling does not mean giving the model unrestricted access to Python functions.

The application remains in control.

### Testing Tool Permissions

I added tests for permission behavior, including:

- Tools that run automatically
- Tools that require approval
- Unknown tools defaulting to approval

Run:

```bash
python -m pytest tests/test_tool_permissions.py -v
```

## 5. SQLite

Part 1 stored long-term memory in a JSON file.

That was useful because JSON made persistence easy to understand:

```text
Agent
  ↓
long_term_memory.py
  ↓
long_term_memory.json
```

In Part 2, I replaced the JSON storage layer with SQLite.

Python includes SQLite support through the built-in:

```python
import sqlite3
```

So I did not need to install or run a separate database server.

The database file is:

```text
agent.db
```

### Database Structure

The SQLite database contains a `memories` table.

Conceptually:

```text
memories

id | key             | value
|--|--
1  | favorite_number | 7
2  | favorite_drink  | coffee
```

The table stores:

- `id` — database row ID
- `key` — unique memory key
- `value` — stored memory value

The database layer lives in:

```text
database.py
```

It handles operations such as:

```text
CREATE → save_memory()
READ   → load_memories()
UPDATE → update_memory()
DELETE → delete_memory()
```

### Inspecting the Database

The database can be inspected directly with the SQLite command-line tool:

```bash
sqlite3 agent.db
```

Then:

```sql
.tables
.schema memories

.headers on
.mode column

SELECT * FROM memories;
```

Exit with:

```text
.quit
```

This was useful because it made the agent's persistent memory less mysterious.

At the database level, it is simply structured data stored in rows.

## 6. Database-Backed Memory

I wanted to change the storage implementation without forcing the rest of the agent to understand SQLite.

So I kept:

```text
long_term_memory.py
```

as the agent-facing memory layer.

The architecture became:

```text
Gemini
  ↓
manual_agent.py
  ↓
tools/registry.py
  ↓
long_term_memory.py
  ↓
database.py
  ↓
agent.db
  ↓
memories table
```

This separation is important.

`long_term_memory.py` answers questions such as:

```text
What should save_memory() return?
Does this memory key already exist?
What message should the agent receive?
```

`database.py` handles:

```text
How is the data inserted?
How is it selected?
How is it updated?
How is it deleted?
```

The rest of the agent does not need to know the SQL details.

### Agent-Facing vs Database Functions

One naming distinction became important during this migration.

The agent-facing read function is:

```python
load_long_term_memory()
```

The database-layer read function is:

```python
load_memories()
```

Conceptually:

```text
Agent
  ↓
load_long_term_memory()
  ↓
database.load_memories()
  ↓
SQLite
```

Keeping the layers separate makes it easier to change the storage implementation without changing every part of the agent.

## 7. Migrating from JSON to SQLite

The final database step was moving existing memory from:

```text
long_term_memory.json
```

to:

```text
agent.db
```

Instead of manually recreating every memory, I used a one-time migration process.

Conceptually:

```text
long_term_memory.json
        ↓
Read JSON
        ↓
Loop through key/value pairs
        ↓
database.save_memory()
        ↓
agent.db
```

After verifying the data in SQLite, the JSON file was no longer the active long-term memory store.

I kept it only as a temporary backup during the migration.


### Why Keep Runtime Databases Out of Git?

The SQLite database contains runtime/user data.

It is not part of the reusable agent template.

So files such as these should remain local:

```text
agent.db
test_agent.db
long_term_memory.json
long_term_memory.json.backup
```

Example `.gitignore` additions:

```gitignore
# Local agent memory / runtime data
memory.json
long_term_memory.json
long_term_memory.json.backup

# SQLite databases / runtime data
agent.db
test_agent.db
*.db-journal
```

I intentionally do not ignore every `*.db` file because a future project might include a database fixture or example database that should be committed.

## Database Testing

I added dedicated SQLite tests.

Instead of testing against the real:

```text
agent.db
```

the tests use:

```text
test_agent.db
```

Conceptually:

```text
pytest
  ↓
test_agent.db
  ↓
run database operations
  ↓
verify results
  ↓
delete test database
```

This prevents tests from modifying real long-term memory.

The database tests cover:

- Saving and loading memory
- Updating memory
- Updating a missing memory
- Deleting memory
- Deleting a missing memory

Run:

```bash
python -m pytest tests/test_database.py -v
```

The existing memory tests were also updated so they test the SQLite-backed implementation instead of JSON storage.

## Running All Tests

After adding the new Phase 2 features, run the complete test suite:

```bash
python -m pytest -v
```

This verifies the original Part 1 functionality together with:

```text
File Reading
External API
Tool Permissions
Human Approval behavior
SQLite Database
Database-Backed Memory
```

## Updated Project Structure

Part 2 adds several files to the original architecture:

```text
ai-agent-google/
├── .env.example
├── .gitignore
├── README.md
├── requirements.txt
│
├── config.py
├── database.py
├── logger.py
├── long_term_memory.py
├── main.py
├── manual_agent.py
├── memory.py
├── prompts.py
│
├── tools/
│   ├── __init__.py
│   ├── calculator.py
│   ├── declarations.py
│   ├── file_reader.py
│   ├── registry.py
│   ├── time_tool.py
│   ├── tool_permissions.py
│   └── weather.py
│
└── tests/
    ├── test_calculator.py
    ├── test_database.py
    ├── test_file_reader.py
    ├── test_memory.py
    ├── test_registry.py
    ├── test_tool_permissions.py
    └── test_weather.py
```

The main additions in Part 2 are:

```text
database.py
tools/file_reader.py
tools/weather.py
tools/tool_permissions.py

tests/test_database.py
tests/test_file_reader.py
tests/test_tool_permissions.py
tests/test_weather.py
```

## What I Learned in Phase 2

Part 1 helped me understand:

```text
User
 ↓
Gemini
 ↓
Tool Request
 ↓
Python Function
 ↓
Tool Result
 ↓
Gemini
 ↓
Answer
```

Part 2 extended that idea.

Now the agent can interact with:

```text
Local Files
External APIs
Persistent Databases
```

while the application controls those interactions through:

```text
Tool Registry
Tool Permissions
Human Approval
Tests
```

The bigger architecture now looks like:

```text
                         ┌→ Calculator
                         │
User → Gemini → Tool ────┼→ File Reader
                         │
                         ├→ Weather API
                         │
                         └→ Memory Tools
                                ↓
                         Permission Check
                                ↓
                      Human Approval if needed
                                ↓
                       long_term_memory.py
                                ↓
                          database.py
                                ↓
                            SQLite
```

The biggest lesson for me was that an agent is not just about adding more tools.

As tools gain the ability to read external information or modify persistent data, the application also needs control over:

- What tools exist
- Which tools can run automatically
- Which tools require approval
- How persistent data is stored
- How those behaviors are tested

## References

Resources used while learning and building this phase include:

- Google Gemini API documentation
- Google Gen AI Python SDK
- Gemini Function Calling documentation
- Python `sqlite3` documentation
- Open-Meteo API documentation
- pytest documentation

This project was built as a hands-on learning exercise. The code and structure evolved through experimentation, debugging, testing, and conversations with ChatGPT.
