from .base_agent import BaseAgent
from typing import List

class ReviewAgent(BaseAgent):
    """Specialist agent for auditing and critiquing QA reports."""
    
    def __init__(self, name: str = "QA_Review_Specialist"):
        super().__init__(
            name=name,
            role_description="Expert in QA standards and auditing. Responsible for ensuring reports are comprehensive, accurate, and actionable."
        )

    async def audit_reports(self, reports: List[str]) -> str:
        """Critiques the gathered reports."""
        all_reports = "\n\n".join(reports)
        prompt = f"""
        Audit the following QA specialist reports. Identify any missing coverage, inaccuracies, or areas for improvement.
        
        Reports:
        {all_reports}
        
        Provide a concise audit summary.
        """
        return await self.chat(prompt)

    def get_system_prompt(self) -> str:
        base_prompt = super().get_system_prompt()
        return base_prompt + "\nFocus on rigor, adherence to standards, and identifying 'unknown unknowns' that specialists might have missed."
