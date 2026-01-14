import requests
import json

payload = {
    "flow": {
        "id": "flow123",
        "name": "Happy Path Flow",
        "start_task": "task1",
        "tasks": [
            {"name": "task1", "description": "Fetch data"},
            {"name": "task2", "description": "Process data"},
            {"name": "task3", "description": "Store data"}
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
    "input_data": {"user_id": 999}
}

try:
    response = requests.post("http://localhost:8000/execute", json=payload)
    print("Status Code:", response.status_code)
    print("Response Text:")
    print(response.text)
except Exception as e:
    print(e)
