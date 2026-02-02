from ..core.base_agent import BaseAgent
from ..skills.security_scanning_skill import SecurityScanningSkill
from ..skills.threat_modeling_skill import ThreatModelingSkill
from ..core.tool_registry import registry
from typing import Optional
import os

class SecurityAgent(BaseAgent):
    """Specialist agent for automated security audits."""
    
    def __init__(self, name: Optional[str] = None):
        name = name or os.getenv("SECURITY_AGENT_NAME", "Security_Specialist")
        super().__init__(
            name=name,
            role_description="Expert in application security, penetration testing, and vulnerability assessment."
        )
        # Register skills
        self.scan_skill = SecurityScanningSkill()
        self.threat_skill = ThreatModelingSkill()
        registry.register_skill(self.scan_skill)
        registry.register_skill(self.threat_skill)

    async def perform_security_audit(self, target: str) -> str:
        """Skill: Performs a SAST/DAST audit."""
        result = await self.execute_tool("security_scan", target=target)
        output = result.output
        if len(output) > 3000:
            output = output[:3000] + "\n... [Security Result Truncated] ..."
            
        if result.success:
            return output
        else:
            return f"Security audit failed: {result.error}\nPartial Output: {output}"

    async def generate_threat_model(self, requirements: str) -> str:
        """Skill: Generates a threat model."""
        result = await self.execute_tool("threat_model", requirements=requirements)
        output = result.output
        if len(output) > 3000:
            output = output[:3000] + "\n... [Threat Model Truncated] ..."
            
        if result.success:
            return output
        else:
            return f"Threat modeling failed: {result.error}\nPartial Output: {output}"

    def get_system_prompt(self) -> str:
        base_prompt = super().get_system_prompt()
        return base_prompt + "\nFocus on threat vectors, data privacy, authentication flows, and ensuring the application is resilient to common attacks."
