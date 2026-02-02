from dotenv import load_dotenv
load_dotenv()

import asyncio
import json
import logging
from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from src.core.orchestrator import QAOrchestrator
from src.core.state import QAOrganizationState

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("QA_Server")

app = FastAPI(title="Agentic QA Organization API")

# CORS for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class MissionRequest(BaseModel):
    input: str

@app.get("/health")
async def health():
    return {"status": "healthy"}

async def mission_event_generator(mission_input: str):
    """
    Generator that runs the LangGraph and yields state updates and logs.
    """
    orchestrator = QAOrchestrator()
    graph = orchestrator.compile()
    
    initial_state = {
        "input": mission_input,
        "reports": [],
        "current_task": "start",
        "visited_agents": [],
        "final_report": ""
    }

    # Signal start
    yield f"data: {json.dumps({'event': 'start', 'message': f'Starting mission: {mission_input}'})}\n\n"

    try:
        # Stream the graph execution
        async for output in graph.astream(initial_state):
            if not output:
                continue
            
            # output is a dict where keys are node names
            node_name = list(output.keys())[0]
            node_data = output[node_name]
            
            # Convert node_data to a JSON-serializable format if it contains Pydantic models
            def serialize(obj):
                if hasattr(obj, "dict"):
                    return obj.dict()
                if hasattr(obj, "model_dump"):
                    return obj.model_dump()
                return str(obj)

            payload = {
                "event": "node_update",
                "node": node_name,
                "message": f"Agent {node_name} completed work.",
                "data": json.loads(json.dumps(node_data, default=serialize))
            }
            yield f"data: {json.dumps(payload)}\n\n"
            
            await asyncio.sleep(0.1)

        yield f"data: {json.dumps({'event': 'complete', 'message': 'Mission finished successfully.'})}\n\n"
        
    except Exception as e:
        logger.error(f"Error during mission execution: {e}")
        yield f"data: {json.dumps({'event': 'error', 'message': str(e)})}\n\n"

@app.post("/mission/stream")
async def stream_mission(request: MissionRequest):
    """
    Endpoint that returns a Server-Sent Events (SSE) stream of the mission execution.
    """
    return StreamingResponse(
        mission_event_generator(request.input),
        media_type="text/event-stream"
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
