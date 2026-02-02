from .skill import Skill, SkillResult
from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage
import logging

logger = logging.getLogger("LoadTestingSkill")

class LoadTestingSkill(Skill):
    """A skill that generates k6 load testing scripts from requirements."""
    
    def __init__(self):
        super().__init__(
            name="generate_load_test",
            description="Generates k6 performance test scripts from requirements or SLOs. Args: requirements (str)"
        )
        self.llm = ChatOpenAI(model="gpt-4o", temperature=0.2)

    async def run(self, requirements: str) -> SkillResult:
        try:
            prompt = f"""
            Identify performance testing requirements and generate a k6 load test script (JavaScript) for the following:
            
            Requirements/SLOs:
            {requirements}
            
            Include virtual users, duration, and thresholds for response times and error rates.
            Provide ONLY the k6 script within a javascript code block.
            """
            
            messages = [
                SystemMessage(content="You are a performance engineer expert in k6 and application scaling."),
                HumanMessage(content=prompt)
            ]
            
            response = await self.llm.ainvoke(messages)
            return SkillResult(
                success=True,
                output=response.content,
                metadata={"framework": "k6", "language": "javascript"}
            )
        except Exception as e:
            logger.error(f"Error in LoadTestingSkill: {e}")
            return SkillResult(success=False, output="", error=str(e))
