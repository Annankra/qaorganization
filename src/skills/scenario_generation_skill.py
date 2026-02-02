from .skill import Skill, SkillResult
from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage
import logging

logger = logging.getLogger("ScenarioGenerationSkill")

class ScenarioGenerationSkill(Skill):
    """A skill that generates functional test scenarios from requirements."""
    
    def __init__(self):
        super().__init__(
            name="generate_scenarios",
            description="Generates functional test scenarios (Gherkin style) from requirements or feature specs. Args: requirements (str)"
        )
        self.llm = ChatOpenAI(model="gpt-4o", temperature=0.7)

    async def run(self, requirements: str) -> SkillResult:
        try:
            prompt = f"""
            Generate a set of comprehensive functional test scenarios in Gherkin (Given/When/Then) format for the following requirements:
            
            {requirements}
            
            Focus on happy paths, edge cases, and error handling.
            """
            
            messages = [
                SystemMessage(content="You are a QA expert in functional test design."),
                HumanMessage(content=prompt)
            ]
            
            response = await self.llm.ainvoke(messages)
            return SkillResult(
                success=True,
                output=response.content,
                metadata={"requirements_length": len(requirements)}
            )
        except Exception as e:
            logger.error(f"Error in ScenarioGenerationSkill: {e}")
            return SkillResult(success=False, output="", error=str(e))
