from ..core.base_agent import BaseAgent
from ..skills.scenario_generation_skill import ScenarioGenerationSkill
from ..core.tool_registry import registry

class FunctionalAgent(BaseAgent):
    """Specialist agent for functional testing and regression."""
    
    def __init__(self, name: str = "Functional_Specialist"):
        super().__init__(
            name=name,
            role_description="Expert in functional testing, manual testing strategies, and regression suite management."
        )
        # Register skills to the global registry or keep them local to the agent
        self.scenario_skill = ScenarioGenerationSkill()
        registry.register_skill(self.scenario_skill)

    async def generate_test_plan(self, requirements: str) -> str:
        """Skill: Generates a functional test plan."""
        result = await self.execute_tool("generate_scenarios", requirements=requirements)
        if result.success:
            return result.output
        else:
            return f"Failed to generate scenarios: {result.error}"

    def get_system_prompt(self) -> str:
        base_prompt = super().get_system_prompt()
        return base_prompt + "\nFocus on business logic correctness, user expectations, and comprehensive coverage of functional requirements."
