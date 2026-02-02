import asyncio
import os
from dotenv import load_dotenv
from src.agents.qa_lead_agent import QALeadAgent
from src.agents.unit_static_agent import UnitStaticAgent
from src.core.knowledge_base import kb
from rich.console import Console
from rich.panel import Panel

load_dotenv()
console = Console()

async def demo():
    console.print(Panel("[bold green]Agentic QA Organization Demo[/bold green]"))
    
    # 1. Initialize Agents
    lead = QALeadAgent()
    unit_specialist = UnitStaticAgent()
    
    # 2. Setup Knowledge Base (Example ingestion)
    # We'll ingest the conversation as a requirement
    if os.path.exists("conversation.txt"):
        kb.ingest_directory(".")
    
    # 3. Simulate a new feature request
    feature_input = "Implement a new authentication module with JWT. Ensure it's secure and follows our standards."
    
    console.print(f"\n[bold blue]Step 1: Lead Agent analyzing feature:[/bold blue] {feature_input}")
    mission = await lead.analyze_and_plan(feature_input)
    
    console.print(f"[bold yellow]Mission Created:[/bold yellow]")
    console.print(f"  - Priority: {mission.priority}")
    console.print(f"  - Risk Score: {mission.risk_score}")
    console.print(f"  - Target Agents: {mission.target_agents}")
    console.print(f"  - Objectives: {mission.objectives}")
    
    # 4. Simulate Handoff to Specialist
    if "UnitStatic" in mission.target_agents or "Security" in mission.target_agents:
        console.print(f"\n[bold blue]Step 2: Assigning tasks to specialist...[/bold blue]")
        await lead.assign_tasks(mission)
        
        console.print(f"\n[bold purple]Step 3: Unit Specialist performing tasks...[/bold purple]")
        lint_result = await unit_specialist.run_lint("src/agents/qa_lead_agent.py")
        console.print(f"  - {lint_result}")
        
        coverage_report = await unit_specialist.analyze_coverage()
        console.print(f"  - {coverage_report}")
    
    console.print("\n[bold green]Demo Complete![/bold green]")

if __name__ == "__main__":
    asyncio.run(demo())
