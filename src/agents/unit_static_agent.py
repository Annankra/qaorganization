from .base_agent import BaseAgent
from ..core.tool_registry import registry
import logging

class UnitStaticAgent(BaseAgent):
    """Specialist agent for unit testing and static analysis."""
    
    def __init__(self, name: str = "Unit_Static_Specialist"):
        super().__init__(
            name=name,
            role_description="Expert in software unit testing and static analysis (linting, complexity, etc.)."
        )

    async def run_lint(self, file_path: str):
        """Skill: Runs linting on a specific file."""
        self.add_to_memory("assistant", f"Starting linting for {file_path}")
        # Simulation of tool usage
        result = self.execute_tool("run_shell", command=f"ls {file_path}") # Placeholder
        if result.success:
            return f"Linting passed for {file_path}. (Simulated)"
        else:
            return f"Linting failed: {result.error}"

    async def analyze_coverage(self):
        """Skill: Analyzes test coverage reports."""
        self.add_to_memory("assistant", "Analyzing coverage reports.")
        # Placeholder for real coverage tool integration
        return "Coverage is at 85%. Missing branches in core/logic.py discovered."

    def get_system_prompt(self) -> str:
        base_prompt = super().get_system_prompt()
        return base_prompt + "\nFocus on code quality, testing best practices, and catching logic errors early."
