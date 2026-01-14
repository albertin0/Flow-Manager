# Flow Design Explanation

## 1. Task Dependency
In this system, task dependency is **sequential and conditional**.
- Tasks do not know about each other directly.
- The **Flow Engine** orchestrates dependencies using a "State Machine" approach.
- A task executes, returns a result (Success/Failure), and the engine looks up the **Conditions** to decide which task to run next.
- For example, `task2` depends on `task1` implicitly because the condition says: "If `task1` is Success, go to `task2`".

## 2. Evaluation
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

## 3. Flow Outcomes
- **Next Task**: The flow continues to the specified task name.
- **End**: The flow terminates gracefully (`target_task_success` or `failure` = "end").
- **Failure**: If a task fails and the condition directs to "end" (or no condition is found), the flow stops, and the overall execution status is marked as failed/completed based on the last state.
