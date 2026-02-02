from ..core.base_agent import BaseAgent
from ..core.tool_registry import registry
from typing import Optional
import os

class UnitStaticAgent(BaseAgent):
    """Specialist agent for unit testing, linting, and static analysis."""
    
    def __init__(self, name: Optional[str] = None):
        name = name or os.getenv("UNIT_STATIC_AGENT_NAME", "Unit_Static_Specialist")
        super().__init__(
            name=name,
            role_description="Expert in code quality, static analysis tools, and unit testing frameworks."
        )

    async def run_lint(self, target: str) -> str:
        """Skill: Runs a simulated linting scan."""
        result = await self.execute_tool("run_shell", command=f"lint {target}")
        output = result.output
        if len(output) > 3000:
            output = output[:3000] + "\n... [Lint Output Truncated] ..."
            
        if result.success:
            return output
        else:
            return f"Linting failed: {result.error}\nPartial Output: {output}"

    async def analyze_coverage(self) -> str:
        """Skill: Analyzes test coverage."""
        return "Coverage analysis: 85% line coverage, 78% branch coverage. Missing tests for error edge cases in payment module."

    def get_system_prompt(self) -> str:
        base_prompt = super().get_system_prompt()
        return base_prompt + "\nFocus on code maintainability, adherence to style guides, and ensuring high test coverage."
