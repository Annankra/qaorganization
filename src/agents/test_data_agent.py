from ..core.base_agent import BaseAgent
from typing import Optional, List, Dict
import os

class TestDataAgent(BaseAgent):
    """
    Expert Software QA and Test Data Engineer agent.
    Responsible for designing, generating, and validating high-quality test data.
    """
    
    def __init__(self, name: Optional[str] = None):
        name = name or os.getenv("TEST_DATA_AGENT_NAME", "Test_Data_Specialist")
        
        description = """
        Highly experienced Software QA and Test Data Engineer. 
        Expert in designing, generating, and validating production-grade test data strategies.
        Focuses on data integrity, coverage, privacy, compliance, and automation.
        """
        
        super().__init__(
            name=name,
            role_description=description
        )

    def get_system_prompt(self) -> str:
        base_prompt = super().get_system_prompt()
        
        expert_prompt = """
        Your primary responsibilities are to design, generate, manage, and validate high-quality test data that accurately reflects real-world production scenarios.

        Think like someone who has owned QA and test data strategy for large, distributed systems.
        Prioritize data integrity, coverage, edge cases, and operational practicality.
        Consider performance, scalability, and maintainability.

        Focus Areas:
        1. Test Data Strategy: end-to-end strategies across unit, integration, system, regression, and performance environments.
        2. Production-like Data Generation: Synthetic or masked/anonymized datasets mirroring production distributions and volumes.
        3. Data Privacy & Compliance: GDPR/CCPA/PII/PCI compliance via masking/anonymization.
        4. Automation & CI/CD: Deterministic, reproducible data lifecycle (creation, refresh, teardown).
        5. Complex Testing: Load, stress, chaos, and migration data preparation.
        6. Observability & Governance: Data quality checks, drift monitoring, and set documentation.

        Task: Given requirements, propose a concrete test data strategy, technical design, specific dataset examples (sample rows/objects), and call out risks/constraints.
        """
        
        return base_prompt + "\n" + expert_prompt

    async def generate_data_strategy(self, requirements: str) -> str:
        """Generates a comprehensive test data strategy for the given requirements."""
        prompt = f"""
        Requirements: {requirements}
        
        Based on these requirements, provide a detailed Test Data Strategy and Design.
        Include:
        - Strategy for happy paths and edge cases.
        - Technical design for data generation (tools, architecture).
        - Specific dataset examples (JSON/SQL/CSV format).
        - Privacy and security considerations.
        - Risk analysis.
        """
        return await self.chat(prompt)
