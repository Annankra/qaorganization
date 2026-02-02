from ..core.base_agent import BaseAgent
from ..skills.load_testing_skill import LoadTestingSkill
from ..core.tool_registry import registry

class PerformanceAgent(BaseAgent):
    """Specialist agent for performance, load, and scalability testing."""
    
    def __init__(self, name: str = "Performance_Specialist"):
        super().__init__(
            name=name,
            role_description="Expert in performance engineering, identifying bottlenecks, and ensuring system scalability."
        )
        # Register skills
        self.load_skill = LoadTestingSkill()
        registry.register_skill(self.load_skill)

    async def plan_performance_test(self, requirements: str) -> str:
        """Skill: Generates a load test plan and script."""
        result = await self.execute_tool("generate_load_test", requirements=requirements)
        if result.success:
            return result.output
        else:
            return f"Performance test planning failed: {result.error}"

    def get_system_prompt(self) -> str:
        base_prompt = super().get_system_prompt()
        return base_prompt + "\nFocus on throughput, latency, resource utilization, and identifying breaking points of the system."
