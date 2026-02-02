from .skill import Skill, SkillResult
from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage
import logging

logger = logging.getLogger("MultiMetricAnalysisSkill")

class MultiMetricAnalysisSkill(Skill):
    """A skill that analyzes performance metrics to identify bottlenecks."""
    
    def __init__(self):
        super().__init__(
            name="analyze_metrics",
            description="Analyzes performance metrics (latency, error rate, CPU/Mem) and provides insights. Args: metrics_summary (str)"
        )
        self.llm = ChatOpenAI(model="gpt-4o", temperature=0.3)

    async def run(self, metrics_summary: str) -> SkillResult:
        try:
            prompt = f"""
            Analyze the following performance metrics and identify potential bottlenecks, scalability issues, or regressions.
            
            Metrics Summary:
            {metrics_summary}
            
            Provide a clear analysis of the system's performance and suggest specific optimizations.
            """
            
            messages = [
                SystemMessage(content="You are a performance optimization expert."),
                HumanMessage(content=prompt)
            ]
            
            response = await self.llm.ainvoke(messages)
            return SkillResult(
                success=True,
                output=response.content,
                metadata={"impact_level": "analyzed"}
            )
        except Exception as e:
            logger.error(f"Error in MultiMetricAnalysisSkill: {e}")
            return SkillResult(success=False, output="", error=str(e))
