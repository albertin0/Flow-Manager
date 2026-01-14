from typing import List, Optional, Any, Dict
from pydantic import BaseModel

class TaskDefinition(BaseModel):
    name: str
    description: Optional[str] = None
    parameters: Optional[Dict[str, Any]] = {}

class Condition(BaseModel):
    name: str
    description: Optional[str] = None
    source_task: str
    outcome: str
    target_task_success: str
    target_task_failure: str

class FlowDefinition(BaseModel):
    id: str
    name: str
    start_task: str
    tasks: List[TaskDefinition]
    conditions: List[Condition]

class FlowInput(BaseModel):
    flow: FlowDefinition
    input_data: Optional[Dict[str, Any]] = {}

class TaskResult(BaseModel):
    task_name: str
    status: str  # "success" or "failure"
    data: Optional[Dict[str, Any]] = None
    trace: Optional[str] = None

class FlowExecutionResult(BaseModel):
    flow_id: str
    status: str # "completed", "failed"
    history: List[TaskResult]
