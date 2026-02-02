from ..core.base_agent import BaseAgent
from typing import List, Optional
import os

class ReviewAgent(BaseAgent):
    """Specialist agent for auditing and critiquing QA reports."""
    
    def __init__(self, name: Optional[str] = None):
        name = name or os.getenv("REVIEWER_NAME", "QA_Review_Specialist")
        super().__init__(
            name=name,
            role_description="Senior QA Manager, responsible for ensuring all specialist reports are accurate, actionable, and meet quality standards."
        )

    async def audit_reports(self, reports: List[str]) -> str:
        """Critiques the gathered reports."""
        # Truncate reports to stay under token limits
        truncated_reports = [r[:5000] + "\n...[truncated]..." if len(r) > 5000 else r for r in reports]
        all_reports = "\n\n".join(truncated_reports)
        
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
