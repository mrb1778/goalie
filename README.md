# Goalie

**Goal Based Programming** in Python.

Goalie is a task execution, dependency injection, and data pipelining framework. It allows you to define functional "Goals" and seamlessly orchestrate them. With Goalie, your tasks can be run directly in Python, triggered via automatically generated command-line arguments, or served dynamically as REST API endpoints—all from the exact same code definition.

---

## Features

- **Goal-Oriented Execution**: Express complex pipelines as declarative, manageable sub-goals.
- **Dependency Injection**: Map input values to the parameters of target tasks dynamically.
- **CLI Generation**: Automatically parses and exposes your goals to the terminal using `argparse`.
- **FastAPI Integration**: Turn any goal into an HTTP endpoint instantly.
- **Standard Library Included**: Common operations like loop, collect, merge, reduce, if, etc., are available out-of-the-box.

---

## Installation

Goalie requires **Python 3.13** or higher. Install it using `pip` from your local clone:

```bash
pip install -e .
```

This will automatically install dependencies listed in `pyproject.toml` (such as `fastapi`, `starlette`, `numpy`, `pandas`, and `xutils`).

---

## Core Concepts

### Goal Manager

The `GoalManager` is the orchestrator. It manages registries of `GoalDefinition`s across multiple logical *scopes*, resolves required parameters, and handles goal invocations.

```python
from goalie import goal

# The default GoalManager is accessible as `goal` and it provides tools to register and run tasks.
```

### Defining a Goal

Use the `@goal(...)` decorator to wrap a standard Python function into a Goal. 

```python
from goalie import goal

@goal(scope="my_scope")
def greet(name: str) -> str:
    return f"Hello, {name}!"
```

### Running Goals

You can invoke goals directly using the manager's `run(...)` method, injecting parameters on the fly:

```python
from goalie import goal

result = goal.run("greet", scope="my_scope", name="Goalie")
print(result) # Outputs: Hello, Goalie!
```

Goals can specify preconditions (`pre`), postconditions (`post`), and refer to other goals, making it easy to create complex execution graphs.

---

## Advanced Usage

### 1. Command Line Interface (CLI)

Goalie easily transforms your functions into CLI-ready applications without writing repetitive `argparse` boilerplate. It automatically discovers parameters and builds arguments.

```python
# main.py
from goalie import goal, run_from_arg_parse

@goal()
def process_data(input_file: str, verbose: bool = False):
    pass

if __name__ == "__main__":
    run_from_arg_parse(goal_manager=goal, default_goal="process_data")
```

Run from terminal:

```bash
python main.py --goal process_data --input_file data.csv --verbose
```

### 2. Goal Server (FastAPI)

Serve your registered goals instantly over HTTP. Goalie maps goal parameters to JSON request payloads and exposes them effortlessly.

To start the server, simply run it using an ASGI runner like `uvicorn`:

```bash
uvicorn goalie.goal_server:app --reload
```

Then you can trigger a goal (e.g., the `print` goal from standard lib) via HTTP POST:

```bash
curl -X POST "http://localhost:8000/goals/run/print" \
     -H "Content-Type: application/json" \
     -d '{"params": {"what": "Hello HTTP!"}}'
```

Endpoints available out of the box:
- `GET /goals/list`: List all goals
- `GET /goals/inputs/{goal_name}`: Inspect parameters required for a goal
- `POST /goals/run/{goal_name}`: Execute a goal

### 3. The Standard Library

Goalie ships with `std_lib.py`, which provides built-in goals under the `"std"` scope. Example goals include:
- Base: `echo`, `print`, `dict`, `range`, `get`, `set`
- Control flows: `if`, `equals`, `gt`, `lt`, `and`, `or`
- Math operations: `multiply`, `add`, `subtract`, `divide`, `avg`
- Collections/loops: `loop`, `collect`, `merge`, `reduce`

---

## License

This project is licensed under the Apache License. See the `LICENSE` file for more details.
