from ..core.base_agent import BaseAgent
from ..skills.security_scanning_skill import SecurityScanningSkill
from ..core.tool_registry import registry

class SecurityAgent(BaseAgent):
    """Specialist agent for security testing (SAST, DAST, Pen-testing)."""
    
    def __init__(self, name: str = "Security_Specialist"):
        super().__init__(
            name=name,
            role_description="Expert in software security, identifying vulnerabilities, and verifying security posture."
        )
        # Register skills
        self.scan_skill = SecurityScanningSkill()
        registry.register_skill(self.scan_skill)

    async def perform_security_audit(self, target: str) -> str:
        """Skill: Performs a SAST/DAST audit."""
        result = await self.execute_tool("security_scan", target=target)
        if result.success:
            return result.output
        else:
            return f"Security audit failed: {result.error}"

    def get_system_prompt(self) -> str:
        base_prompt = super().get_system_prompt()
        return base_prompt + "\nFocus on threat vectors, data privacy, authentication flows, and ensuring the application is resilient to common attacks."
