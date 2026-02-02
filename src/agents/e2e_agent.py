from ..core.base_agent import BaseAgent
from ..skills.user_journey_mapping_skill import UserJourneyMappingSkill
from ..core.tool_registry import registry

class E2EAgent(BaseAgent):
    """Specialist agent for end-to-end and system-wide testing."""
    
    def __init__(self, name: str = "E2E_Specialist"):
        super().__init__(
            name=name,
            role_description="Expert in end-to-end testing, user journey validation, and system integration flows."
        )
        # Register skills
        self.mapping_skill = UserJourneyMappingSkill()
        registry.register_skill(self.mapping_skill)

    async def define_journeys(self, requirements: str) -> str:
        """Skill: Identifies critical user journeys."""
        result = await self.execute_tool("map_user_journeys", requirements=requirements)
        if result.success:
            return result.output
        else:
            return f"Failed to map journeys: {result.error}"

    def get_system_prompt(self) -> str:
        base_prompt = super().get_system_prompt()
        return base_prompt + "\nFocus on the complete user experience, cross-service interactions, and validating that the main business goals are achievable."
