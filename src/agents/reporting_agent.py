from ..core.base_agent import BaseAgent
from ..skills.testrail_sync_skill import TestRailSyncSkill
from ..core.tool_registry import registry
from typing import List, Dict, Any, Optional
import os
import json
import datetime

class ReportingAgent(BaseAgent):
    """Specialist agent for aggregating and synthesizing QA mission reports."""
    
    def __init__(self, name: Optional[str] = None):
        name = name or os.getenv("REPORTER_NAME", "QA_Reporting_Specialist")
        super().__init__(
            name=name,
            role_description="Expert in technical communication and QA metrics summary. Responsible for creating executive reports."
        )
        self.testrail_skill = TestRailSyncSkill()
        registry.register_skill(self.testrail_skill)

    async def sync_to_testrail(self, reports: List[str]):
        """Parses reports and syncs identified case results to TestRail."""
        # Simple extraction logic: look for "Case ID: \d+" in reports
        # In a real scenario, this would be more structured.
        results = []
        for r in reports:
            # Mock extraction for demonstration
            if "Case ID: 101" in r:
                results.append({"case_id": 101, "status_id": 1 if "PASS" in r else 5, "comment": "Verified via agent"})
        
        if results:
            return await self.testrail_skill.run(
                project_id=1, # Default project
                suite_id=1,   # Default suite
                run_name=f"Mission Run {datetime.datetime.now().strftime('%Y-%m-%d')}",
                results=results
            )
        return "No TestRail cases identified in reports."

    async def generate_final_summary(self, reports: List[str], input_data: str) -> str:
        """Synthesizes multiple specialist reports into a single executive summary."""
        # Truncate individual reports to stay within a reasonable token budget
        truncated_reports = [self._truncate_report(r) for r in reports]
        all_reports = "\n\n".join(truncated_reports)
        
        prompt = f"""
        Synthesize the following QA specialist reports and evaluations into a single executive summary.
        
        Original Input/Requirement:
        {input_data}
        
        Specialist Reports & Audits:
        {all_reports}
        
        The summary should include:
        1. Overview of testing performed.
        2. Critical findings and risks.
        3. Go/No-Go recommendation based on the findings.
        4. Remediation roadmap.
        
        Format it in clean Markdown.
        """
        return await self.chat(prompt)

    def _truncate_report(self, content: str, max_chars: int = 3000) -> str:
        """Truncates a report string if it exceeds the character limit."""
        if len(content) > max_chars:
            return content[:max_chars] + "\n... [Report Truncated due to size] ..."
        return content

    def get_system_prompt(self) -> str:
        base_prompt = super().get_system_prompt()
        return base_prompt + "\nYour goal is to provide a clear, professional, and actionable summary for stakeholders."
