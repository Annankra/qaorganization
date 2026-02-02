from ..core.base_agent import BaseAgent
from ..skills.user_journey_mapping_skill import UserJourneyMappingSkill
from ..skills.playwright_automation_skill import PlaywrightAutomationSkill
from ..core.tool_registry import registry
from typing import Optional
import os

class E2EAgent(BaseAgent):
    """Specialist agent for end-to-end testing and automation."""
    
    def __init__(self, name: Optional[str] = None):
        name = name or os.getenv("E2E_AGENT_NAME", "E2E_Specialist")
        super().__init__(
            name=name,
            role_description="Expert in user journey mapping and automated E2E testing using Playwright."
        )
        # Register skills
        self.mapping_skill = UserJourneyMappingSkill()
        self.automation_skill = PlaywrightAutomationSkill()
        registry.register_skill(self.mapping_skill)
        registry.register_skill(self.automation_skill)

    async def define_journeys(self, requirements: str) -> str:
        """Skill: Identifies critical user journeys."""
        result = await self.execute_tool("map_user_journeys", requirements=requirements)
        if result.success:
            return result.output
        else:
            return f"Failed to map journeys: {result.error}"

    async def generate_automation(self, journey: str) -> str:
        """Skill: Generates Playwright automation code."""
        result = await self.execute_tool("generate_playwright_test", journey_description=journey)
        if result.success:
            return result.output
        else:
            return f"Failed to generate automation: {result.error}"

    def get_system_prompt(self) -> str:
        base_prompt = super().get_system_prompt()
        return base_prompt + "\nFocus on the complete user experience, cross-service interactions, and validating that the main business goals are achievable."
