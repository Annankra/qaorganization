from typing import Dict, Any
from langgraph.graph import StateGraph, END
from .state import QAOrganizationState
from ..agents.qa_lead_agent import QALeadAgent

class QAOrchestrator:
    """Sets up and manages the LangGraph for the QA organization."""
    
    def __init__(self):
        self.lead_agent = QALeadAgent()
        self.workflow = StateGraph(QAOrganizationState)
        self._build_graph()

    def _build_graph(self):
        """Defines the graph nodes and edges."""
        
        # Define Nodes
        self.workflow.add_node("lead_planner", self._lead_planner_node)
        self.workflow.add_node("finalizer", self._finalizer_node)
        
        # Define Edges
        self.workflow.set_entry_point("lead_planner")
        
        # For now, a direct path. We will add specialist nodes in subsequent tasks.
        self.workflow.add_edge("lead_planner", "finalizer")
        self.workflow.add_edge("finalizer", END)

    async def _lead_planner_node(self, state: QAOrganizationState) -> Dict[str, Any]:
        """Node for the Lead Agent to analyze and plan."""
        mission = await self.lead_agent.analyze_and_plan(state["input"])
        return {"mission": mission}

    async def _finalizer_node(self, state: QAOrganizationState) -> Dict[str, Any]:
        """Node to aggregate all reports and conclude the mission."""
        summary = f"QA Mission complete for {mission.priority} priority task. " if (mission := state.get("mission")) else "Mission failed."
        reports_summary = "\n".join(state.get("reports", []))
        return {"final_report": f"{summary}\n\nReports:\n{reports_summary}"}

    def compile(self):
        return self.workflow.compile()
