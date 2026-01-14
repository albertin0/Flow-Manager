from fastapi import FastAPI, HTTPException
from models import FlowInput, FlowExecutionResult
from engine import FlowEngine

app = FastAPI(title="Flow Manager Microservice", description="Generic sequential task execution engine")

engine = FlowEngine()

@app.post("/execute", response_model=FlowExecutionResult)
async def execute_flow(flow_input: FlowInput):
    """
    Execute a flow defined in the request body.
    """
    try:
        result = engine.execute_flow(flow_input.flow, flow_input.input_data)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
def home():
    return {"message": "Flow Manager Service is running. Use POST /execute to run flows."}
