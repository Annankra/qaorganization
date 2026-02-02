from ..core.skill import Skill, SkillResult
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
import logging
import subprocess

logger = logging.getLogger("SecurityScanningSkill")

class SecurityScanningSkill(Skill):
    """A skill that wraps SAST/DAST concepts for security analysis."""
    
    def __init__(self):
        super().__init__(
            name="security_scan",
            description="Performs security scanning (SAST/DAST) on a code snippet or endpoint. Args: target (str), scan_type (str)"
        )
        self.llm = ChatOpenAI(model="gpt-4o", temperature=0.2)

    async def run(self, target: str, scan_type: str = "SAST") -> SkillResult:
        try:
            # Here we simulate or wrap real tools. 
            # For this implementation, we'll use the LLM to 'analyze' the target for common vulnerabilities 
            # as a stand-in for complex tool output parsing.
            prompt = f"""
            Perform a {scan_type} security analysis on the following target:
            
            Target:
            {target}
            
            Identify potential vulnerabilities (e.g., OWASP Top 10, SQLi, XSS, insecure dependencies).
            Provide a summary of findings and remediation steps.
            """
            
            messages = [
                SystemMessage(content="You are a security expert specialized in SAST and DAST."),
                HumanMessage(content=prompt)
            ]
            
            response = await self.llm.ainvoke(messages)
            return SkillResult(
                success=True,
                output=response.content,
                metadata={"scan_type": scan_type, "target_type": "code/endpoint"}
            )
        except Exception as e:
            logger.error(f"Error in SecurityScanningSkill: {e}")
            return SkillResult(success=False, output="", error=str(e))
