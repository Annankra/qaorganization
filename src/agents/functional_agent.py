from ..skills.scenario_generation_skill import ScenarioGenerationSkill
from ..skills.regression_analysis_skill import RegressionAnalysisSkill
from ..core.tool_registry import registry

class FunctionalAgent(BaseAgent):
    """Specialist agent for functional testing and regression."""
    
    def __init__(self, name: str = "Functional_Specialist"):
        super().__init__(
            name=name,
            role_description="Expert in functional testing, manual testing strategies, and regression suite management."
        )
        # Register skills
        self.scenario_skill = ScenarioGenerationSkill()
        self.regression_skill = RegressionAnalysisSkill()
        registry.register_skill(self.scenario_skill)
        registry.register_skill(self.regression_skill)

    async def generate_test_plan(self, requirements: str) -> str:
        """Skill: Generates a functional test plan."""
        result = await self.execute_tool("generate_scenarios", requirements=requirements)
        if result.success:
            return result.output
        else:
            return f"Failed to generate scenarios: {result.error}"

    async def analyze_regression_needs(self, changes: str, suite_summary: str) -> str:
        """Skill: Analyzes regression needs."""
        result = await self.execute_tool("analyze_regression", change_description=changes, existing_tests_summary=suite_summary)
        if result.success:
            return result.output
        else:
            return f"Failed to analyze regression: {result.error}"

    def get_system_prompt(self) -> str:
        base_prompt = super().get_system_prompt()
        return base_prompt + "\nFocus on business logic correctness, user expectations, and comprehensive coverage of functional requirements."
