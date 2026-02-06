from ..core.base_agent import BaseAgent
from ..skills.scenario_generation_skill import ScenarioGenerationSkill
from ..skills.regression_analysis_skill import RegressionAnalysisSkill
from ..skills.test_case_management_skill import TestCaseManagementSkill
from ..core.tool_registry import registry
from typing import Optional, List, Dict
import os
import json

class FunctionalAgent(BaseAgent):
    """Specialist agent for functional testing and regression."""
    
    def __init__(self, name: Optional[str] = None, specialization: Optional[str] = None):
        self.specialization = specialization
        name = name or os.getenv("FUNCTIONAL_AGENT_NAME", "Functional_Specialist")
        
        role_map = {
            "architect": "Senior QA Architect focused on high-level test strategy, coverage gaps, and structural integrity of the test suite.",
            "detail": "Meticulous QA Specialist with extreme attention to detail, edge cases, boundary values, and UI/UX subtleties.",
            "business": "Business-focused QA Analyst who ensures requirements meet user expectations and business logic is bulletproof."
        }
        
        description = role_map.get(specialization, "Expert in functional testing, manual testing strategies, and regression suite management.")
        
        super().__init__(
            name=name,
            role_description=description
        )
        # Register skills
        self.scenario_skill = ScenarioGenerationSkill()
        self.regression_skill = RegressionAnalysisSkill()
        self.upload_skill = TestCaseManagementSkill()
        registry.register_skill(self.scenario_skill)
        registry.register_skill(self.regression_skill)
        registry.register_skill(self.upload_skill)

    async def generate_test_plan(self, requirements: str) -> str:
        """Skill: Generates a functional test plan."""
        result = await self.execute_tool("generate_scenarios", requirements=requirements)
        if result.success:
            return result.output
        else:
            return f"Failed to generate scenarios: {result.error}"

    async def analyze_regression_needs(self, changes: str, suite_summary: str) -> str:
        """Skill: Analyzes regression needs."""
        result = await self.execute_tool("analyze_regression", change_description=changes, existing_tests_summary=suite_summary)
        if result.success:
            return result.output
        else:
            return f"Failed to analyze regression: {result.error}"

    async def parse_scenarios_to_structured_data(self, markdown_report: str) -> List[Dict]:
        """Uses LLM to structure markdown scenarios into JSON for TestRail."""
        prompt = f"""
        Convert the following functional test scenarios into a structured JSON list for TestRail.
        
        Markdown Report:
        {markdown_report}
        
        Respond ONLY with a JSON list where each object has these fields:
        - "title": Short descriptive title
        - "preconditions": Relevant setup info
        - "steps": Numbered steps
        - "expected": The expected outcome
        
        Example:
        [
          {{
            "title": "Login Success",
            "preconditions": "Valid user exists",
            "steps": "1. Enter username\\n2. Enter password",
            "expected": "User is logged in"
          }}
        ]
        """
        response = await self.chat(prompt)
        try:
            clean_json = response.strip().replace("```json", "").replace("```", "")
            return json.loads(clean_json)
        except Exception as e:
            self.add_to_memory("assistant", f"Error parsing scenarios to JSON: {e}")
            return []

    def get_system_prompt(self) -> str:
        base_prompt = super().get_system_prompt()
        
        specialization_prompts = {
            "architect": "Focus on global coverage, integration points, and high-level scenario architecture. Ensure scenarios are reusable and well-structured.",
            "detail": "Focus on the 'unhappy path', negative testing, edge cases, and tiny details that others might miss. Be extremely thorough with verification steps.",
            "business": "Focus on the end-user perspective and business value. Ensure that every scenario directly validates a core business requirement or user goal."
        }
        
        focus = specialization_prompts.get(self.specialization, "Focus on business logic correctness, user expectations, and comprehensive coverage of functional requirements.")
        return base_prompt + f"\n{focus}"
