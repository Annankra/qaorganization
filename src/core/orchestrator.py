from .state import QAOrganizationState
from ..agents.qa_lead_agent import QALeadAgent
from ..agents.unit_static_agent import UnitStaticAgent
from ..agents.review_agent import ReviewAgent
from ..agents.functional_agent import FunctionalAgent
from ..agents.e2e_agent import E2EAgent
from ..agents.security_agent import SecurityAgent
from ..agents.performance_agent import PerformanceAgent

class QAOrchestrator:
    """Sets up and manages the LangGraph for the QA organization."""
    
    def __init__(self):
        self.lead_agent = QALeadAgent()
        self.unit_static_agent = UnitStaticAgent()
        self.functional_agent = FunctionalAgent()
        self.e2e_agent = E2EAgent()
        self.security_agent = SecurityAgent()
        self.performance_agent = PerformanceAgent()
        self.review_agent = ReviewAgent()
        self.workflow = StateGraph(QAOrganizationState)
        self._build_graph()

    def _build_graph(self):
        """Defines the graph nodes and edges."""
        
        # Define Nodes
        self.workflow.add_node("lead_planner", self._lead_planner_node)
        self.workflow.add_node("unit_static_node", self._unit_static_node)
        self.workflow.add_node("functional_node", self._functional_node)
        self.workflow.add_node("e2e_node", self._e2e_node)
        self.workflow.add_node("security_node", self._security_node)
        self.workflow.add_node("performance_node", self._performance_node)
        self.workflow.add_node("reviewer", self._reviewer_node)
        self.workflow.add_node("finalizer", self._finalizer_node)
        
        # Define Edges
        self.workflow.set_entry_point("lead_planner")
        
        # Conditional dynamic routing
        self.workflow.add_conditional_edges(
            "lead_planner",
            self._route_tasks,
            {
                "unit_static": "unit_static_node",
                "functional": "functional_node",
                "e2e": "e2e_node",
                "security": "security_node",
                "performance": "performance_node",
                "end": "finalizer"
            }
        )
        
        self.workflow.add_edge("unit_static_node", "reviewer")
        self.workflow.add_edge("functional_node", "reviewer")
        self.workflow.add_edge("e2e_node", "reviewer")
        self.workflow.add_edge("security_node", "reviewer")
        self.workflow.add_edge("performance_node", "reviewer")
        self.workflow.add_edge("reviewer", "finalizer")
        self.workflow.add_edge("finalizer", END)

    def _route_tasks(self, state: QAOrganizationState) -> str:
        """Determines which specialist agent to route to."""
        mission = state.get("mission")
        if not mission or not mission.target_agents:
            return "end"
        
        # Simple routing logic for now
        if "UnitStatic" in mission.target_agents:
            return "unit_static"
        if "Functional" in mission.target_agents:
            return "functional"
        if "E2E" in mission.target_agents:
            return "e2e"
        if "Security" in mission.target_agents:
            return "security"
        if "Performance" in mission.target_agents:
            return "performance"
        
        return "end"

    async def _unit_static_node(self, state: QAOrganizationState) -> Dict[str, Any]:
        """Node for the UnitStaticAgent."""
        # Simulated run of the agent's logic
        lint_report = await self.unit_static_agent.run_lint(state["input"])
        coverage_report = await self.unit_static_agent.analyze_coverage()
        report = f"--- Unit & Static Analysis Report ---\n{lint_report}\n{coverage_report}"
        return {"reports": [report]}

    async def _functional_node(self, state: QAOrganizationState) -> Dict[str, Any]:
        """Node for the FunctionalAgent."""
        # 1. Generate new scenarios
        scenarios = await self.functional_agent.generate_test_plan(state["input"])
        
        # 2. Analyze regression needs (simulation with a generic suite summary)
        mock_suite = "Login tests, User profile tests, JWT Validation tests, Session timeout tests."
        regression = await self.functional_agent.analyze_regression_needs(state["input"], mock_suite)
        
        report = f"--- Functional Test Scenarios ---\n{scenarios}\n\n--- Regression Analysis ---\n{regression}"
        return {"reports": [report]}

    async def _e2e_node(self, state: QAOrganizationState) -> Dict[str, Any]:
        """Node for the E2EAgent."""
        # 1. Map journeys
        journeys = await self.e2e_agent.define_journeys(state["input"])
        
        # 2. Generate automation for the first journey (simulation)
        automation = await self.e2e_agent.generate_automation(journeys)
        
        report = f"--- Critical User Journeys ---\n{journeys}\n\n--- Playwright Automation ---\n{automation}"
        return {"reports": [report]}

    async def _security_node(self, state: QAOrganizationState) -> Dict[str, Any]:
        """Node for the SecurityAgent."""
        # 1. Generate threat model
        threat_model = await self.security_agent.generate_threat_model(state["input"])
        
        # 2. Perform security audit
        audit = await self.security_agent.perform_security_audit(state["input"])
        
        report = f"--- Threat Modeling Analysis ---\n{threat_model}\n\n--- Security Audit Findings ---\n{audit}"
        return {"reports": [report]}

    async def _performance_node(self, state: QAOrganizationState) -> Dict[str, Any]:
        """Node for the PerformanceAgent."""
        plan = await self.performance_agent.plan_performance_test(state["input"])
        report = f"--- Performance Load Test Plan ---\n{plan}"
        return {"reports": [report]}

    async def _reviewer_node(self, state: QAOrganizationState) -> Dict[str, Any]:
        """Node for the ReviewAgent to audit gather reports."""
        audit_report = await self.review_agent.audit_reports(state.get("reports", []))
        report = f"--- Quality Audit Report ---\n{audit_report}"
        return {"reports": [report]}

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
