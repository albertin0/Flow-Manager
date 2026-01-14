# Flow Manager Microservice

A generic, sequential task execution engine built with FastAPI. This service allows you to define workflows in JSON and execute them via an API.

## Features
- **Sequential Execution**: Run tasks one after another.
- **Conditional Logic**: Branching based on task outcomes (success/failure).
- **Extensible**: Add new tasks by registering Python functions.

## Project Structure
- `main.py`: The FastAPI application entry point.
- `engine.py`: Core logic for parsing and executing flows.
- `tasks.py`: Definitions of available tasks (`task1`, `task2`, `task3`).
- `models.py`: Pydantic models for request/response schemas.

## Installation

1. Install dependencies:
   ```bash
   python -m venv .venv
   .venv\Scripts\activate
   pip install -r requirements.txt
   ```

## Running the Service

Start the server using Uvicorn:
```bash
uvicorn main:app --reload
```
The API will be available at `http://localhost:8000`.

## API Usage

### Execute a Flow
**Endpoint**: `POST /execute`

**Payload Example**:
```json
{
  "flow": {
    "id": "flow1",
    "name": "My Flow",
    "start_task": "task1",
    "tasks": [
      { "name": "task1" },
      { "name": "task2" },
      { "name": "task3" }
    ],
    "conditions": [
      {
        "name": "c1",
        "source_task": "task1",
        "outcome": "success",
        "target_task_success": "task2",
        "target_task_failure": "end"
      },
      {
        "name": "c2",
        "source_task": "task2",
        "outcome": "success",
        "target_task_success": "task3",
        "target_task_failure": "end"
      }
    ]
  },
  "input_data": { "foo": "bar" }
}
```

## Running Tests
Run the verification script to see a live example:
```bash
python verify_flow.py
```

Run the failure scenario test:
```bash
python verify_flow_2.py
```

## Flow Design Explanation

### 1. Task Dependency
In this system, task dependency is **sequential and conditional**.
- Tasks do not know about each other directly.
- The **Flow Engine** orchestrates dependencies using a "State Machine" approach.
- A task executes, returns a result (Success/Failure), and the engine looks up the **Conditions** to decide which task to run next.
- For example, `task2` depends on `task1` implicitly because the condition says: "If `task1` is Success, go to `task2`".

### 2. Evaluation
Success or failure is determined by the `TaskResult` object returned by the python function implementation.
- **Success**: `status="success"`
- **Failure**: `status="failure"` (or any unhandled exception)

The `Condition` object in the JSON defines how to interpret these results:
```json
{
  "source_task": "task1",
  "outcome": "success",
  "target_task_success": "task2",
  "target_task_failure": "end"
}
```
- If `task1` returns "success", the engine transitions to `target_task_success` (`task2`).
- If `task1` returns anything else (e.g. "failure"), it transitions to `target_task_failure` (`end` or error handler).

### 3. Flow Outcomes
- **Next Task**: The flow continues to the specified task name.
- **End**: The flow terminates gracefully (`target_task_success` or `failure` = "end").
- **Failure**: If a task fails and the condition directs to "end" (or no condition is found), the flow stops, and the overall execution status is marked as failed/completed based on the last state.
