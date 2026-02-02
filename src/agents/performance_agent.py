from ..core.base_agent import BaseAgent
from ..skills.load_testing_skill import LoadTestingSkill
from ..skills.multi_metric_analysis_skill import MultiMetricAnalysisSkill
from ..skills.test_execution_skill import TestExecutionSkill
from ..core.tool_registry import registry
from typing import Optional
import os

class PerformanceAgent(BaseAgent):
    """Specialist agent for performance, load, and scalability testing."""
    
    def __init__(self, name: Optional[str] = None):
        name = name or os.getenv("PERFORMANCE_AGENT_NAME", "Performance_Specialist")
        super().__init__(
            name=name,
            role_description="Expert in performance engineering, identifying bottlenecks, and ensuring system scalability."
        )
        # Register skills
        self.load_skill = LoadTestingSkill()
        self.analysis_skill = MultiMetricAnalysisSkill()
        self.execution_skill = TestExecutionSkill()
        registry.register_skill(self.load_skill)
        registry.register_skill(self.analysis_skill)
        registry.register_skill(self.execution_skill)

    async def plan_performance_test(self, requirements: str) -> str:
        """Skill: Generates a load test plan and script."""
        result = await self.execute_tool("generate_load_test", requirements=requirements)
        if result.success:
            return result.output
        else:
            return f"Performance test planning failed: {result.error}"

    async def execute_load_test(self, code: str) -> str:
        """Skill: Executes k6 load test script."""
        result = await self.execute_tool("execute_test", code=code, test_type="k6")
        
        # Truncate output to avoid massive token usage in downstream agents
        max_log_size = 3000
        output = result.output
        if len(output) > max_log_size:
            output = output[:max_log_size] + "\n... [Output Truncated for Brevity] ..."

        if result.success:
            return f"Load Test SUCCESS:\n{output}"
        else:
            return f"Load Test FAILED:\n{output}\nError: {result.error}"

    async def analyze_performance_results(self, metrics: str) -> str:
        """Skill: Analyzes performance metrics."""
        result = await self.execute_tool("analyze_metrics", metrics_summary=metrics)
        if result.success:
            return result.output
        else:
            return f"Performance analysis failed: {result.error}"

    def get_system_prompt(self) -> str:
        base_prompt = super().get_system_prompt()
        return base_prompt + "\nFocus on throughput, latency, resource utilization, and identifying breaking points of the system."
