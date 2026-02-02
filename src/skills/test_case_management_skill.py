from ..core.skill import Skill, SkillResult
from ..core.mcp_client import testrail_mcp
import logging

logger = logging.getLogger("TestCaseManagementSkill")

class TestCaseManagementSkill(Skill):
    """
    A skill that manages test cases in TestRail via MCP.
    """
    
    def __init__(self):
        super().__init__(
            name="upload_test_cases",
            description="Uploads a list of structured test cases to TestRail. Args: section_id (int), test_cases (list of dicts with title, preconditions, steps, expected)"
        )

    async def run(self, section_id: int, test_cases: list) -> SkillResult:
        """
        Loops through cases and calls the MCP tool for each.
        """
        try:
            results = []
            for case in test_cases:
                out = await testrail_mcp.call_tool("add_test_case", {
                    "section_id": section_id,
                    "title": case.get("title", "Untitled Case"),
                    "custom_preconds": case.get("preconditions", ""),
                    "custom_steps": case.get("steps", ""),
                    "expected": case.get("expected", "")
                })
                results.append(out)
            
            final_output = f"Bulk Upload Results for Section {section_id}:\n" + "\n".join(results)
            return SkillResult(success=True, output=final_output)
            
        except Exception as e:
            logger.error(f"Error in TestCaseManagementSkill: {e}")
            return SkillResult(success=False, output="", error=str(e))
