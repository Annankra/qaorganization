import asyncio
import sys
import os
from dotenv import load_dotenv

# Load environment variables (OPENAI_API_KEY) before any project imports
# This ensures singletons like KnowledgeBase can access environment variables during import.
load_dotenv()

from src.core.orchestrator import QAOrchestrator
from src.core.ci_bridge import CIBridge
from rich.console import Console
from rich.markdown import Markdown

console = Console()

async def run_mission(input_text: str, **kwargs):
    """Triggers a full QA mission via the orchestrator."""
    console.print(f"[bold blue]Starting QA Mission for:[/bold blue] {input_text}\n")
    
    orchestrator = QAOrchestrator()
    app = orchestrator.compile()
    
    # Initialize state
    initial_state = {
        "input": input_text,
        "reports": [],
        "current_task": "start",
        "visited_agents": [],
        "manual_agents": kwargs.get("manual_agents"),
        "final_report": ""
    }
    
    # Run the graph
    console.print("[yellow]Agents are collaborating...[/yellow]")
    final_output = await app.ainvoke(initial_state)
    
    # Display final report
    console.print("\n[bold green]Mission Complete![/bold green]\n")
    report_md = Markdown(final_output["final_report"])
    console.print(report_md)
    
    # Check CI Gate (Simulated)
    # Extract score from report (mock logic for demo)
    # In reality, the EvalAgent node would return a structured object in the state
    console.print("\n[bold cyan]CI/CD Gate Status:[/bold cyan]")
    if "Score: 8" in final_output["final_report"] or "Score: 9" in final_output["final_report"] or "Score: 10" in final_output["final_report"]:
        console.print("[green]PASS: Quality Gate Met[/green]")
    else:
        console.print("[red]FAIL: Quality Gate Not Met - Requires Human Review[/red]")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Run a QA Mission")
    parser.add_argument("--mission", type=str, help="The QA mission goal")
    parser.add_argument("--agents", type=str, help="Comma-separated list of manual agents (UnitStatic, Functional, E2E, Security, Performance)")
    parser.add_argument("unnamed_mission", type=str, nargs="?", help="The QA mission goal (positional)")
    
    args = parser.parse_args()
    
    mission = args.mission or args.unnamed_mission or "Implement a new JWT-based authentication system for the user profile service."
    manual_agents = args.agents.split(",") if args.agents else None
        
    asyncio.run(run_mission(mission, manual_agents=manual_agents))
