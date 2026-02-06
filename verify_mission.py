import asyncio
import httpx
import json

async def run_test_mission():
    url = "http://localhost:8000/mission/stream"
    payload = {"input": "User authentication with MFA and password recovery"}
    
    print(f"Starting mission: {payload['input']}")
    
    async with httpx.AsyncClient(timeout=None) as client:
        async with client.stream("POST", url, json=payload) as response:
            async for line in response.aiter_lines():
                if line.startswith("data: "):
                    data = json.loads(line[6:])
                    event = data.get("event")
                    node = data.get("node")
                    message = data.get("message")
                    
                    if event == "node_update":
                        print(f"[{node}] {message}")
                    elif event == "complete":
                        print(f"Mission complete: {message}")
                    elif event == "error":
                        print(f"Error: {message}")

if __name__ == "__main__":
    try:
        asyncio.run(run_test_mission())
    except KeyboardInterrupt:
        pass
