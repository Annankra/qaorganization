from ..core.skill import Skill, SkillResult
from ..core.mcp_client import testrail_mcp
import logging

logger = logging.getLogger("TestRailSyncSkill")

class TestRailSyncSkill(Skill):
    """
    A skill that synchronizes QA results with TestRail via MCP.
    """
    
    def __init__(self):
        super().__init__(
            name="sync_to_testrail",
            description="Synchronizes mission results with TestRail. Args: project_id (int), suite_id (int), run_name (str), results (list of dicts with case_id, status_id, comment)"
        )

    async def run(self, project_id: int, suite_id: int, run_name: str, results: list) -> SkillResult:
        """
        Creates a test run and adds multiple results.
        """
        try:
            # 1. Create a Test Run
            run_output = await testrail_mcp.call_tool("create_test_run", {
                "project_id": project_id,
                "suite_id": suite_id,
                "name": run_name
            })
            
            if "Successfully created Test Run" not in run_output:
                return SkillResult(success=False, output=f"Failed to create Test Run: {run_output}")

            # Extract run_id from output (naive parsing)
            # Output format: "Successfully created Test Run: Name (ID: 123)"
            run_id_part = run_output.split("(ID: ")[1]
            run_id = int(run_id_part.replace(")", "").strip())
            
            # 2. Add results for each case
            sync_summaries = []
            for result in results:
                res_output = await testrail_mcp.call_tool("add_test_result", {
                    "run_id": run_id,
                    "case_id": result["case_id"],
                    "status_id": result["status_id"],
                    "comment": result["comment"]
                })
                sync_summaries.append(res_output)
            
            final_output = f"Sync Summary for Run {run_id}:\n" + "\n".join(sync_summaries)
            return SkillResult(success=True, output=final_output)
            
        except Exception as e:
            logger.error(f"Error in TestRailSyncSkill: {e}")
            return SkillResult(success=False, output="", error=str(e))
