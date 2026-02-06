import os
import datetime
from typing import Dict, Any
from langgraph.graph import StateGraph, END
from .state import QAOrganizationState
from ..agents.qa_lead_agent import QALeadAgent
from ..agents.unit_static_agent import UnitStaticAgent
from ..agents.review_agent import ReviewAgent
from ..agents.functional_agent import FunctionalAgent
from ..agents.test_data_agent import TestDataAgent
from ..agents.e2e_agent import E2EAgent
from ..agents.security_agent import SecurityAgent
from ..agents.performance_agent import PerformanceAgent
from ..agents.eval_agent import EvalAgent
from ..agents.reporting_agent import ReportingAgent
from ..skills.knowledge_ingestion_skill import KnowledgeIngestionSkill

class QAOrchestrator:
    """Sets up and manages the LangGraph for the QA organization."""
    
    def __init__(self):
        self.lead_agent = QALeadAgent()
        self.unit_static_agent = UnitStaticAgent()
        # Initialize 3 Specialist Functional Agents
        self.functional_architect = FunctionalAgent(name="Functional_Architect", specialization="architect")
        self.detail_specialist = FunctionalAgent(name="Detail_Specialist", specialization="detail")
        self.business_expert = FunctionalAgent(name="Business_Expert", specialization="business")
        self.test_data_agent = TestDataAgent()
        self.e2e_agent = E2EAgent()
        self.security_agent = SecurityAgent()
        self.performance_agent = PerformanceAgent()
        self.eval_agent = EvalAgent()
        self.reporting_agent = ReportingAgent()
        self.ingestion_skill = KnowledgeIngestionSkill()
        self.review_agent = ReviewAgent()
        self.workflow = StateGraph(QAOrganizationState)
        self.artifacts_dir = "artifacts"
        os.makedirs(self.artifacts_dir, exist_ok=True)
        self._build_graph()

    def _save_artifact(self, name: str, content: str):
        """Helper to save an artifact to the artifacts directory."""
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{timestamp}_{name}.md"
        filepath = os.path.join(self.artifacts_dir, filename)
        with open(filepath, "w") as f:
            f.write(content)
        # Also maintain a symlink-like current version for easier access if desired
        latest_path = os.path.join(self.artifacts_dir, f"latest_{name}.md")
        with open(latest_path, "w") as f:
            f.write(content)

    def _build_graph(self):
        """Defines the graph nodes and edges."""
        
        # Define Nodes
        self.workflow.add_node("lead_planner", self._lead_planner_node)
        self.workflow.add_node("router_node", self._router_node)
        self.workflow.add_node("unit_static_node", self._unit_static_node)
        self.workflow.add_node("functional_architect_node", self._functional_architect_node)
        self.workflow.add_node("detail_specialist_node", self._detail_specialist_node)
        self.workflow.add_node("business_expert_node", self._business_expert_node)
        self.workflow.add_node("test_data_node", self._test_data_node)
        self.workflow.add_node("e2e_node", self._e2e_node)
        self.workflow.add_node("security_node", self._security_node)
        self.workflow.add_node("performance_node", self._performance_node)
        self.workflow.add_node("functional_consolidator", self._functional_consolidator_node)
        self.workflow.add_node("evaluator", self._evaluator_node)
        self.workflow.add_node("reviewer", self._reviewer_node)
        self.workflow.add_node("finalizer", self._finalizer_node)
        
        # Define Edges
        self.workflow.set_entry_point("lead_planner")
        
        # Lead Planner goes to Router
        self.workflow.add_edge("lead_planner", "router_node")
        
        # Conditional dynamic routing from Router
        self.workflow.add_conditional_edges(
            "router_node",
            self._route_tasks,
            {
                "unit_static": "unit_static_node",
                "functional_architect": "functional_architect_node",
                "detail_specialist": "detail_specialist_node",
                "business_expert": "business_expert_node",
                "test_data": "test_data_node",
                "e2e": "e2e_node",
                "security": "security_node",
                "performance": "performance_node",
                "review": "reviewer",
                "end": "finalizer"
            }
        )
        
        # Specialists go back to Router (not Lead Planner)
        self.workflow.add_edge("unit_static_node", "router_node")
        
        # Parallel Fan-in to Consolidator
        self.workflow.add_edge("functional_architect_node", "functional_consolidator")
        self.workflow.add_edge("detail_specialist_node", "functional_consolidator")
        self.workflow.add_edge("business_expert_node", "functional_consolidator")
        self.workflow.add_edge("test_data_node", "functional_consolidator")
        self.workflow.add_edge("functional_consolidator", "router_node")
        
        self.workflow.add_edge("e2e_node", "router_node")
        self.workflow.add_edge("security_node", "router_node")
        self.workflow.add_edge("performance_node", "router_node")
        self.workflow.add_edge("reviewer", "evaluator")
        self.workflow.add_edge("evaluator", "finalizer")
        self.workflow.add_edge("finalizer", END)

    def _route_tasks(self, state: QAOrganizationState) -> str:
        """Determines which specialist agent to route to."""
        mission = state.get("mission")
        if not mission or not mission.target_agents:
            return "end"
        
        visited = state.get("visited_agents", [])
        manual_agents = state.get("manual_agents")
        
        # Use manual selection if provided, otherwise use AI-planned target_agents
        targets = manual_agents if manual_agents is not None else mission.target_agents
        
        for agent in targets:
            if agent == "UnitStatic" and "UnitStatic" not in visited:
                return "unit_static"
            if agent == "Functional" and "Functional" not in visited:
                return ["functional_architect", "detail_specialist", "business_expert", "test_data"]
            if agent == "E2E" and "E2E" not in visited:
                return "e2e"
            if agent == "Security" and "Security" not in visited:
                return "security"
            if agent == "Performance" and "Performance" not in visited:
                return "performance"
        
        # If all target agents visited, go to review
        if state.get("reports"):
            return "review"
            
        return "end"

    async def _unit_static_node(self, state: QAOrganizationState) -> Dict[str, Any]:
        """Node for the UnitStaticAgent."""
        # Simulated run of the agent's logic
        lint_report = await self.unit_static_agent.run_lint(state["input"])
        coverage_report = await self.unit_static_agent.analyze_coverage()
        report = f"--- Unit & Static Analysis Report ---\n{lint_report}\n{coverage_report}"
        self._save_artifact("unit_static_report", report)
        return {"reports": [report], "visited_agents": ["UnitStatic"]}

    async def _functional_architect_node(self, state: QAOrganizationState) -> Dict[str, Any]:
        """Brainstorming: Architect."""
        scenarios = await self.functional_architect.generate_test_plan(state["input"])
        report = f"--- Architect Preliminary Brainstorm ---\n{scenarios}"
        # We store the preliminary report in a temporary state key or just add to reports
        return {"reports": [report], "visited_agents": ["Functional_Architect"]}

    async def _detail_specialist_node(self, state: QAOrganizationState) -> Dict[str, Any]:
        """Brainstorming: Detail Specialist."""
        scenarios = await self.detail_specialist.generate_test_plan(state["input"])
        report = f"--- Detail Specialist Brainstorm ---\n{scenarios}"
        return {"reports": [report], "visited_agents": ["Detail_Specialist"]}

    async def _business_expert_node(self, state: QAOrganizationState) -> Dict[str, Any]:
        """Brainstorming: Business Expert."""
        scenarios = await self.business_expert.generate_test_plan(state["input"])
        report = f"--- Business Expert Brainstorm ---\n{scenarios}"
        return {"reports": [report], "visited_agents": ["Business_Expert"]}

    async def _test_data_node(self, state: QAOrganizationState) -> Dict[str, Any]:
        """Test Data Strategy: Specialist."""
        report = await self.test_data_agent.generate_data_strategy(state["input"])
        self._save_artifact("test_data_report", report)
        return {"reports": [report]}

    async def _functional_consolidator_node(self, state: QAOrganizationState) -> Dict[str, Any]:
        """Consolidation & Finalization: Architect Collaborates with all specialist findings."""
        input_data = state["input"]
        all_reports = state.get("reports", [])
        
        architect_scenarios = next((r for r in all_reports if "Architect Preliminary" in r), "")
        detail_scenarios = next((r for r in all_reports if "Detail Specialist Brainstorm" in r), "")
        business_scenarios = next((r for r in all_reports if "Business Expert Brainstorm" in r), "")
        test_data_report = next((r for r in all_reports if "Test Data Strategy" in r or "dataset examples" in r.lower()), "No test data strategy generated.")
        
        # Consolidation Phase
        consolidation_prompt = f"""
        You are the Quality Architect. You are leading a team of specialists to design a comprehensive testing mission.
        
        We have findings from three functional specialists and one Test Data specialist:
        
        ARCHITECT:
        {architect_scenarios}
        
        DETAIL SPECIALIST:
        {detail_scenarios}
        
        BUSINESS EXPERT:
        {business_scenarios}
        
        TEST DATA STRATEGY:
        {test_data_report}
        
        Requirement: {input_data}
        
        Your task is to collaborate and merge these into a single, world-class, production-grade functional test plan.
        Ensure you include the meticulous details from the Detail Specialist, the business value from the Business Expert, AND the production-grade test data strategy.
        Remove redundancies and ensure comprehensive coverage.
        """
        
        final_scenarios = await self.functional_architect.chat(consolidation_prompt)
        
        # Analyze regression needs
        from ..core.knowledge_base import kb
        context = kb.get_context_summary(input_data)
        regression = await self.functional_architect.analyze_regression_needs(input_data, context)
        
        report = f"--- Functional Test Scenarios (Collaborative Effort) ---\n{final_scenarios}\n\n--- Regression Analysis ---\n{regression}"
        self._save_artifact("functional_report", report)

        # Automated Test Case Upload to TestRail
        structured_cases = await self.functional_architect.parse_scenarios_to_structured_data(final_scenarios)
        if structured_cases:
            upload_result = await self.functional_architect.upload_skill.run(
                section_id=1, # Default section
                test_cases=structured_cases
            )
            self._save_artifact("testrail_case_upload_status", str(upload_result.output))
        
        return {"reports": [report], "visited_agents": ["Functional"]}

    async def _e2e_node(self, state: QAOrganizationState) -> Dict[str, Any]:
        """Node for the E2EAgent."""
        # 1. Map journeys
        journeys = await self.e2e_agent.define_journeys(state["input"])
        
        # 2. Generate automation
        automation = await self.e2e_agent.generate_automation(journeys)
        
        # 3. Execute automation
        execution_results = await self.e2e_agent.execute_automation(automation)
        
        report = f"--- Critical User Journeys ---\n{journeys}\n\n--- Playwright Automation ---\n{automation}\n\n--- Execution Results ---\n{execution_results}"
        self._save_artifact("e2e_report", report)
        return {"reports": [report], "visited_agents": ["E2E"]}

    async def _security_node(self, state: QAOrganizationState) -> Dict[str, Any]:
        """Node for the SecurityAgent."""
        # 1. Generate threat model
        threat_model = await self.security_agent.generate_threat_model(state["input"])
        
        # 2. Perform security audit
        audit = await self.security_agent.perform_security_audit(state["input"])
        
        report = f"--- Threat Modeling Analysis ---\n{threat_model}\n\n--- Security Audit Findings ---\n{audit}"
        self._save_artifact("security_report", report)
        return {"reports": [report], "visited_agents": ["Security"]}

    async def _performance_node(self, state: QAOrganizationState) -> Dict[str, Any]:
        """Node for the PerformanceAgent."""
        # 1. Plan load test
        plan = await self.performance_agent.plan_performance_test(state["input"])
        
        # 2. Execute load test
        execution_results = await self.performance_agent.execute_load_test(plan)
        
        # 3. Analyze metrics (using execution results instead of mock metrics)
        analysis = await self.performance_agent.analyze_performance_results(execution_results)
        
        report = f"--- Performance Load Test Plan ---\n{plan}\n\n--- Execution Results ---\n{execution_results}\n\n--- Performance Bottleneck Analysis ---\n{analysis}"
        self._save_artifact("performance_report", report)
        return {"reports": [report], "visited_agents": ["Performance"]}

    async def _evaluator_node(self, state: QAOrganizationState) -> Dict[str, Any]:
        """Node for the EvalAgent to score the mission."""
        eval_result = await self.eval_agent.evaluate_mission(state)
        report = f"--- Mission Evaluation (Score: {eval_result.score}/10) ---\nRationale: {eval_result.rationale}\nFeedback: {', '.join(eval_result.feedback)}"
        self._save_artifact("evaluation_report", report)
        return {"reports": [report]}

    async def _reviewer_node(self, state: QAOrganizationState) -> Dict[str, Any]:
        """Node for the ReviewAgent to audit gather reports."""
        audit_report = await self.review_agent.audit_reports(state.get("reports", []))
        report = f"--- Quality Audit Report ---\n{audit_report}"
        self._save_artifact("quality_audit_report", report)
        return {"reports": [report]}

    async def _lead_planner_node(self, state: QAOrganizationState) -> Dict[str, Any]:
        """Mission Planning: Lead Agent."""
        mission = await self.lead_agent.analyze_and_plan(state["input"])
        # Return manual_agents so UI knows they are persisted
        return {
            "mission": mission, 
            "current_task": "routing",
            "manual_agents": state.get("manual_agents") 
        }

    async def _router_node(self, state: QAOrganizationState) -> Dict[str, Any]:
        """Passive node to handle routing without re-planning."""
        return {"current_task": "routing", "manual_agents": state.get("manual_agents")}

    async def _finalizer_node(self, state: QAOrganizationState) -> Dict[str, Any]:
        """Node to aggregate all reports and conclude the mission."""
        # Use Reporting Agent to synthesize everything
        final_summary = await self.reporting_agent.generate_final_summary(
            reports=state.get("reports", []),
            input_data=state["input"]
        )
        
        # Save to Knowledge Base for learning
        mission_id = f"mission_{hash(state['input'])}"
        await self.ingestion_skill.run(mission_id, final_summary)
        
        self._save_artifact("final_mission_report", final_summary)

        # 3. Synchronize with TestRail
        tr_sync_status = await self.reporting_agent.sync_to_testrail(state.get("reports", []))
        self._save_artifact("testrail_sync_status", str(tr_sync_status.output if hasattr(tr_sync_status, 'output') else tr_sync_status))
        
        return {"final_report": final_summary}

    def compile(self):
        return self.workflow.compile()
