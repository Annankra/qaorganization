from ..core.base_agent import BaseAgent
from ..core.knowledge_base import kb
from ..core.policy_engine import PolicyEngine
from ..skills.jira_ingestion_skill import JiraIngestionSkill
from ..core.tool_registry import registry
from pydantic import BaseModel
from typing import List, Optional
import json
import os

class TestMission(BaseModel):
    priority: str
    target_agents: List[str]
    objectives: List[str]
    risk_score: int

class QALeadAgent(BaseAgent):
    """The orchestrator agent responsible for analyzing requirements and planning missions."""
    
    def __init__(self, name: Optional[str] = None):
        name = name or os.getenv("LEAD_ORCHESTRATOR_NAME", "QA_Lead_Orchestrator")
        super().__init__(
            name=name,
            role_description="Head of Software Quality, responsible for creating QA organizations and processes. Expert in orchestration and risk assessment."
        )
        self.policy_engine = PolicyEngine()
        self.jira_skill = JiraIngestionSkill()
        registry.register_skill(self.jira_skill)

    async def analyze_and_plan(self, input_data: str) -> TestMission:
        """Analyzes input (feature spec, PR) and creates a testing mission."""
        
        # 1. Retrieve relevant history/docs from Knowledge Base
        relevant_docs = kb.search(input_data)
        context = "\n".join([doc.page_content for doc in relevant_docs])
        
        # 2. Perform Risk Assessment and Mission Planning
        prompt = f"""
        Analyze the following input and create a testing mission.
        
        Input: {input_data}
        
        Historical Context & Jira Tickets:
        {context}
        
        Respond ONLY with a JSON object in this format:
        {{
            "priority": "High" | "Medium" | "Low",
            "target_agents": ["UnitStatic", "Functional", "Performance", "Security", etc.],
            "objectives": ["string description of goals"],
            "risk_score": 1-10
        }}
        """
        
        response_text = await self.chat(prompt)
        
        # Basic JSON extraction (naive, could be improved with better parsers)
        try:
            # Clean up potential markdown formatting
            clean_json = response_text.strip().replace("```json", "").replace("```", "")
            mission_data = json.loads(clean_json)
            return TestMission(**mission_data)
        except Exception as e:
            self.add_to_memory("assistant", f"Error parsing mission JSON: {e}")
            # Fallback
            return TestMission(
                priority="Medium",
                target_agents=["Functional"],
                objectives=["Validate basic functionality (failed to parse AI plan)"],
                risk_score=5
            )

    async def assign_tasks(self, mission: TestMission):
        """Logic to route work to specialist agents."""
        # In a real implementation with LangGraph, this would trigger a graph traversal.
        # For now, we simulate the assignment.
        for agent_type in mission.target_agents:
            self.add_to_memory("assistant", f"Assigning '{mission.priority}' task to {agent_type} agent.")
            # Triggering actual agents would happen here.
            
    def get_system_prompt(self) -> str:
        base_prompt = super().get_system_prompt()
        return base_prompt + "\nFocus on high-level strategy, risk mitigation, and ensuring all testing types are considered."
