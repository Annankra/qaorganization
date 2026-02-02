import subprocess
import logging
from typing import Dict, Any, Callable, Optional, List
from pydantic import BaseModel

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("ToolRegistry")

class ToolResult(BaseModel):
    success: bool
    output: str
    error: Optional[str] = None
    metadata: Dict[str, Any] = {}

class ToolRegistry:
    """Central registry for tools that agents can execute."""
    
    def __init__(self):
        self._tools: Dict[str, Callable] = {}
        self._tool_descriptions: Dict[str, str] = {}
        self._setup_default_tools()

    def register_tool(self, name: str, description: str, func: Callable):
        self._tools[name] = func
        self._tool_descriptions[name] = description
        logger.info(f"Registered tool: {name}")

    def get_tool(self, name: str) -> Optional[Callable]:
        return self._tools.get(name)

    def list_tools(self) -> List[Dict[str, str]]:
        return [{"name": name, "description": desc} for name, desc in self._tool_descriptions.items()]

    def execute(self, tool_name: str, **kwargs) -> ToolResult:
        """Executes a tool by name with provided arguments."""
        tool = self.get_tool(tool_name)
        if not tool:
            return ToolResult(success=False, output="", error=f"Tool '{tool_name}' not found.")
        
        try:
            logger.info(f"Executing tool: {tool_name} with args: {kwargs}")
            result = tool(**kwargs)
            if isinstance(result, ToolResult):
                return result
            return ToolResult(success=True, output=str(result))
        except Exception as e:
            logger.error(f"Error executing tool {tool_name}: {e}")
            return ToolResult(success=False, output="", error=str(e))

    def _setup_default_tools(self):
        """Registers some basic system tools."""
        self.register_tool(
            "run_shell",
            "Runs a shell command and returns output. Args: command (str)",
            self._run_shell
        )

    def _run_shell(self, command: str) -> ToolResult:
        try:
            result = subprocess.run(
                command, 
                shell=True, 
                capture_output=True, 
                text=True, 
                check=False
            )
            return ToolResult(
                success=result.returncode == 0,
                output=result.stdout,
                error=result.stderr if result.returncode != 0 else None,
                metadata={"returncode": result.returncode}
            )
        except Exception as e:
            return ToolResult(success=False, output="", error=str(e))

# Singleton instance
registry = ToolRegistry()
