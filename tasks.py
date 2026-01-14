from typing import Any, Dict, Callable
from models import TaskResult

# Simple Registry to map task names to functions
TASK_REGISTRY: Dict[str, Callable] = {}

def register_task(name: str):
    def decorator(func: Callable):
        TASK_REGISTRY[name] = func
        return func
    return decorator

# --- Sample Tasks ---

@register_task("task1")
def fetch_data(context: Dict[str, Any], previous_result: Any = None) -> TaskResult:
    print(f"[Task1] Fetching data... Context: {context}")
    
    if context.get("force_fail"):
        return TaskResult(task_name="task1", status="failure", trace="Simulated failure from input")

    # Simulate fetch logic
    # In a real app, this might fetch from an API or DB
    return TaskResult(task_name="task1", status="success", data={"fetched_item": "sample_data"})

@register_task("task2")
def process_data(context: Dict[str, Any], previous_result: TaskResult) -> TaskResult:
    print(f"[Task2] Processing data... Previous Data: {previous_result.data}")
    if previous_result and previous_result.data:
        processed_item = str(previous_result.data.get("fetched_item", "")).upper()
        return TaskResult(task_name="task2", status="success", data={"processed_item": processed_item})
    
    return TaskResult(task_name="task2", status="failure", trace="No data to process")

@register_task("task3")
def store_data(context: Dict[str, Any], previous_result: TaskResult) -> TaskResult:
    print(f"[Task3] Storing data... Previous Data: {previous_result.data}")
    if previous_result and previous_result.data:
        # Simulate generic storage
        stored_value = previous_result.data.get("processed_item")
        print(f" >> STORED: {stored_value}")
        return TaskResult(task_name="task3", status="success", data={"stored_id": 12345})
    
    return TaskResult(task_name="task3", status="failure", trace="No data to store")

def get_task_function(name: str) -> Callable:
    return TASK_REGISTRY.get(name)
