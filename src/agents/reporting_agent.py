from .base_agent import BaseAgent
from typing import List, Dict, Any

class ReportingAgent(BaseAgent):
    """Specialist agent for aggregating and synthesizing QA mission reports."""
    
    def __init__(self, name: str = "QA_Reporting_Specialist"):
        super().__init__(
            name=name,
            role_description="Expert in technical communication and QA metrics summary. Responsible for creating executive reports."
        )

    async def generate_final_summary(self, reports: List[str], input_data: str) -> str:
        """Synthesizes multiple specialist reports into a single executive summary."""
        all_reports = "\n\n".join(reports)
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

    def get_system_prompt(self) -> str:
        base_prompt = super().get_system_prompt()
        return base_prompt + "\nYour goal is to provide a clear, professional, and actionable summary for stakeholders."
