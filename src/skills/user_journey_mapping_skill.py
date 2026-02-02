from ..core.skill import Skill, SkillResult
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
import logging

logger = logging.getLogger("UserJourneyMappingSkill")

class UserJourneyMappingSkill(Skill):
    """A skill that identifies and maps critical user journeys from requirements."""
    
    def __init__(self):
        super().__init__(
            name="map_user_journeys",
            description="Analyzes requirements to identify critical end-to-end user journeys. Args: requirements (str)"
        )
        self.llm = ChatOpenAI(model="gpt-4o", temperature=0.5)

    async def run(self, requirements: str) -> SkillResult:
        try:
            prompt = f"""
            Based on the following requirements, identify the most critical end-to-end user journeys. 
            For each journey, describe the persona, the goal, and the high-level steps.
            
            Requirements:
            {requirements}
            
            Focus on flows that cross multiple system components or services.
            """
            
            messages = [
                SystemMessage(content="You are a QA specialist focused on user experience and system-wide workflows."),
                HumanMessage(content=prompt)
            ]
            
            response = await self.llm.ainvoke(messages)
            return SkillResult(
                success=True,
                output=response.content,
                metadata={"num_journeys_identified": "dynamic"}
            )
        except Exception as e:
            logger.error(f"Error in UserJourneyMappingSkill: {e}")
            return SkillResult(success=False, output="", error=str(e))
