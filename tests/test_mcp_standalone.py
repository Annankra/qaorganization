import asyncio
import os
import sys

# Ensure project root is in path
sys.path.append(os.getcwd())

from src.core.mcp_client import testrail_mcp

async def test_mcp_connection():
    print("Testing TestRail MCP Connection...")
    # Attempt to call a tool even with dummy data
    # The server should respond even if the underlying API call fails due to credentials
    result = await testrail_mcp.call_tool("create_test_run", {
        "project_id": 1,
        "suite_id": 1,
        "name": "Integration Test Run"
    })
    print(f"Tool Output: {result}")
    await testrail_mcp.close()

if __name__ == "__main__":
    asyncio.run(test_mcp_connection())
