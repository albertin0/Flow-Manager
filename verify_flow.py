import requests
import json
import sys
import time

BASE_URL = "http://localhost:8000"

def test_successful_flow():
    print("\n--- Testing Successful Flow (Fetch -> Process -> Store) ---")
    payload = {
        "flow": {
            "id": "flow123",
            "name": "Data processing flow",
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
        "input_data": {"user_id": 999}
    }
    
    try:
        response = requests.post(f"{BASE_URL}/execute", json=payload)
        response.raise_for_status()
        data = response.json()
        print("Response:", json.dumps(data, indent=2))
        
        # Verification logic
        history = data['history']
        if len(history) == 3 and data['status'] == 'completed':
            print("✅ TEST PASSED: Flow completed successfully with 3 steps.")
        else:
            print("❌ TEST FAILED: Unexpected history length or status.")
            
    except Exception as e:
        print(f"❌ TEST FAILED: Request error - {e}")

def main():
    # Wait for server to be up (manual step usually, but valid for script usage)
    print("Ensure the server is running on localhost:8000 before running this script.")
    test_successful_flow()

if __name__ == "__main__":
    main()
