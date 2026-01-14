import requests
import json
import sys

BASE_URL = "http://localhost:8000"

def test_failure_flow():
    print("\n--- Testing Failure Flow (Fetch Fails -> End) ---")
    payload = {
        "flow": {
            "id": "flow_fail_test",
            "name": "Failure Test Flow",
            "start_task": "task1",
            "tasks": [
                {
                    "name": "task1",
                    "description": "Fetch data"
                },
                {
                    "name": "task2",
                    "description": "Process data"
                },
                {
                    "name": "task3",
                    "description": "Store data"
                }
            ],
            "conditions": [
                {
                    "name": "condition_task1_result",
                    "description": "Evaluate the result of task1. If successful, proceed to task2; otherwise, end the flow.",
                    "source_task": "task1",
                    "outcome": "success",
                    "target_task_success": "task2",
                    "target_task_failure": "end"
                },
                {
                    "name": "condition_task2_result",
                    "description": "Evaluate the result of task2. If successful, proceed to task3; otherwise, end the flow.",
                    "source_task": "task2",
                    "outcome": "success",
                    "target_task_success": "task3",
                    "target_task_failure": "end"
                }
            ]
        },
        "input_data": {"user_id": 999, "force_fail": True}
    }
    
    try:
        response = requests.post(f"{BASE_URL}/execute", json=payload)
        response.raise_for_status()
        data = response.json()
        print("Response:", json.dumps(data, indent=2))
        
        # Verification logic
        history = data['history']
        # We expect only task1 to run and be failed.
        if len(history) == 1 and history[0]['status'] == 'failure' and data['status'] == 'failed':
            print("✅ TEST PASSED: Flow correctly failed and stopped after task1.")
        else:
            print("❌ TEST FAILED: Unexpected history length or status.")
            
    except Exception as e:
        print(f"❌ TEST FAILED: Request error - {e}")

if __name__ == "__main__":
    test_failure_flow()
