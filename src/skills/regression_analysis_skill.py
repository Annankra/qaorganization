from ..core.skill import Skill, SkillResult
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
import logging

logger = logging.getLogger("RegressionAnalysisSkill")

class RegressionAnalysisSkill(Skill):
    """A skill that suggests relevant regression tests based on changes."""
    
    def __init__(self):
        super().__init__(
            name="analyze_regression",
            description="Analyzes changes and selects relevant existing tests from a suite for regression. Args: change_description (str), existing_tests_summary (str)"
        )
        self.llm = ChatOpenAI(model="gpt-4o", temperature=0.3)

    async def run(self, change_description: str, existing_tests_summary: str) -> SkillResult:
        try:
            prompt = f"""
            Given the following change description and a summary of existing functional tests, identify which tests MUST be part of the regression suite to ensure no breakage.
            
            Change Description:
            {change_description}
            
            Existing Tests Summary:
            {existing_tests_summary}
            
            Provide a list of recommended regression tests with a brief rationale for each.
            """
            
            messages = [
                SystemMessage(content="You are a QA expert in regression testing and impact analysis."),
                HumanMessage(content=prompt)
            ]
            
            response = await self.llm.ainvoke(messages)
            return SkillResult(
                success=True,
                output=response.content,
                metadata={"change_impact_level": "analyzed"}
            )
        except Exception as e:
            logger.error(f"Error in RegressionAnalysisSkill: {e}")
            return SkillResult(success=False, output="", error=str(e))
