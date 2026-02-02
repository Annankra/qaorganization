from ..core.skill import Skill, SkillResult
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
import logging

logger = logging.getLogger("ThreatModelingSkill")

class ThreatModelingSkill(Skill):
    """A skill that identifies security threats based on architecture/requirements."""
    
    def __init__(self):
        super().__init__(
            name="threat_model",
            description="Analyzes requirements/architecture to identify potential security threats. Args: requirements (str)"
        )
        self.llm = ChatOpenAI(model="gpt-4o", temperature=0.5)

    async def run(self, requirements: str) -> SkillResult:
        try:
            prompt = f"""
            Perform a threat modeling analysis for the following requirements/system description.
            Identify high-risk areas, potential attack vectors, and recommended security controls.
            
            Requirements:
            {requirements}
            
            Focus on authentication, data protection, and external interfaces.
            """
            
            messages = [
                SystemMessage(content="You are a security architect expert in threat modeling."),
                HumanMessage(content=prompt)
            ]
            
            response = await self.llm.ainvoke(messages)
            return SkillResult(
                success=True,
                output=response.content,
                metadata={"vulnerabilities_identified": "dynamic"}
            )
        except Exception as e:
            logger.error(f"Error in ThreatModelingSkill: {e}")
            return SkillResult(success=False, output="", error=str(e))
