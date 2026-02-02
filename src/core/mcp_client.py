import asyncio
import os
import sys
import logging
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

logger = logging.getLogger("TestRailMCPClient")

class TestRailMCPClient:
    """
    Model Context Protocol client for TestRail.
    Connects to the local MCP server and exposes its tools.
    """
    
    def __init__(self):
        self.server_params = StdioServerParameters(
            command=sys.executable,
            args=[os.path.join(os.getcwd(), "mcp_testrail", "server.py")],
            env=os.environ.copy()
        )
        self.session = None
        self._exit_stack = None

    async def connect(self):
        """Initializes connection to the MCP server."""
        if self.session:
            return
        
        from contextlib import AsyncExitStack
        self._exit_stack = AsyncExitStack()
        
        try:
            read, write = await self._exit_stack.enter_async_context(stdio_client(self.server_params))
            self.session = await self._exit_stack.enter_async_context(ClientSession(read, write))
            await self.session.initialize()
            logger.info("Connected to TestRail MCP Server")
        except Exception as e:
            logger.error(f"Failed to connect to TestRail MCP Server: {e}")
            self.session = None

    async def call_tool(self, name: str, arguments: dict):
        """Calls an MCP tool by name."""
        if not self.session:
            await self.connect()
        
        if not self.session:
            return "Connection failed."
            
        try:
            result = await self.session.call_tool(name, arguments)
            return result.content[0].text if result.content else "No output."
        except Exception as e:
            logger.error(f"Error calling MCP tool {name}: {e}")
            return f"Error: {str(e)}"

    async def close(self):
        """Closes the MCP session."""
        if self._exit_stack:
            await self._exit_stack.aclose()
            self.session = None
            logger.info("TestRail MCP Server connection closed")

# Singleton instance
testrail_mcp = TestRailMCPClient()
