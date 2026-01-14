from typing import List, Dict, Any, Optional
from models import FlowDefinition, TaskResult, FlowExecutionResult, Condition
from tasks import get_task_function

class FlowEngine:
    def execute_flow(self, flow: FlowDefinition, initial_input: Dict[str, Any]) -> FlowExecutionResult:
        current_task_name = flow.start_task
        history: List[TaskResult] = []
        context = initial_input.copy()
        
        print(f"--- Starting Flow: {flow.name} (ID: {flow.id}) ---")
        
        last_result: Optional[TaskResult] = None # Hold result of the immediately preceding task
        
        while current_task_name and current_task_name != "end":
            print(f" -> Executing Task: {current_task_name}")
            
            # Find the task implementation
            task_func = get_task_function(current_task_name)
            if not task_func:
                error_msg = f"Task implementation '{current_task_name}' not found."
                print(f"Error: {error_msg}")
                fail_result = TaskResult(task_name=current_task_name, status="failure", trace=error_msg)
                history.append(fail_result)
                return FlowExecutionResult(flow_id=flow.id, status="failed", history=history)

            # Execute the task
            try:
                # We adhere to the signature: func(context, last_result)
                # For the first task, last_result is None
                result = task_func(context, last_result)
            except Exception as e:
                result = TaskResult(
                    task_name=current_task_name, 
                    status="failure", 
                    trace=f"Exception: {str(e)}"
                )

            history.append(result)
            last_result = result
            
            # Determine next step based on conditions
            next_step = self._evaluate_next_step(current_task_name, result, flow.conditions)
            print(f" <- Task '{current_task_name}' finished with status '{result.status}'. Next step: {next_step}")
            
            current_task_name = next_step
            
        final_status = "completed" if history and history[-1].status == "success" else "failed"
        return FlowExecutionResult(flow_id=flow.id, status=final_status, history=history)

    def _evaluate_next_step(self, current_task_name: str, result: TaskResult, conditions: List[Condition]) -> str:
        # Find condition for this task
        # There might be multiple conditions; this logic assumes simple matching or first match.
        # The user schema implies one condition block per transition logic usually, 
        # but let's look for the one matching the source task.
        
        relevant_conditions = [c for c in conditions if c.source_task == current_task_name]
        
        if not relevant_conditions:
            # If no condition defined, this is a dead end -> implicit end? 
            # Or should we default to end? Let's default to "end".
            return "end"
            
        for condition in relevant_conditions:
            # Check success/failure match
            if condition.outcome == result.status:
                return condition.target_task_success
            else:
                # If the outcome defined in condition was "success" but result was "failure", 
                # we should check if there's an explicit "failure" logic or use the failure target of this condition?
                # The user schema provided:
                # "outcome": "success", "target_task_success": "task2", "target_task_failure": "end"
                # This implies if match `outcome` -> go success path, else -> go failure path
                
                # Check if the condition object handles strict matching or "if/else" logic.
                # The schema keys: 'outcome', 'target_task_success', 'target_task_failure'. 
                # Interpretation: If result.status == condition.outcome, then success_target, else failure_target.
                
                return condition.target_task_failure
                
        return "end"
