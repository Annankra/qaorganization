from .skill import Skill, SkillResult
from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage
import logging

logger = logging.getLogger("PlaywrightAutomationSkill")

class PlaywrightAutomationSkill(Skill):
    """A skill that generates Playwright test scripts from user journeys."""
    
    def __init__(self):
        super().__init__(
            name="generate_playwright_test",
            description="Generates Playwright (Python or JS) test code from a user journey description. Args: journey_description (str)"
        )
        self.llm = ChatOpenAI(model="gpt-4o", temperature=0.2)

    async def run(self, journey_description: str) -> SkillResult:
        try:
            prompt = f"""
            Convert the following user journey description into a functional Playwright (Python) test script. 
            Include necessary imports, setup, and assertions.
            
            User Journey:
            {journey_description}
            
            Provide ONLY the code within a python code block.
            """
            
            messages = [
                SystemMessage(content="You are a QA automation engineer expert in Playwright."),
                HumanMessage(content=prompt)
            ]
            
            response = await self.llm.ainvoke(messages)
            return SkillResult(
                success=True,
                output=response.content,
                metadata={"language": "python", "framework": "playwright"}
            )
        except Exception as e:
            logger.error(f"Error in PlaywrightAutomationSkill: {e}")
            return SkillResult(success=False, output="", error=str(e))
