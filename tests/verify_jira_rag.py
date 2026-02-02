import asyncio
import os
from dotenv import load_dotenv

# Load environment variables early
load_dotenv()

from src.core.knowledge_base import kb
from src.core.jira_connector import jira_connector
from src.agents.qa_lead_agent import QALeadAgent
from langchain_core.documents import Document

async def verify_jira_rag():
    print("--- Verifying Jira RAG Integration ---")
    
    # 1. Create mock Jira issues
    mock_issues = [
        {
            "key": "QA-101",
            "fields": {
                "summary": "Login page fails on mobile devices",
                "description": "Users reporting 404 when clicking login from iPhone 13.",
                "status": {"name": "Open"},
                "issuetype": {"name": "Bug"},
                "priority": {"name": "High"}
            }
        },
        {
            "key": "QA-102",
            "fields": {
                "summary": "Implement MFA for all users",
                "description": "Security requirement: All logins must require a 6-digit TOTP code.",
                "status": {"name": "In Progress"},
                "issuetype": {"name": "Story"},
                "priority": {"name": "Medium"}
            }
        }
    ]
    
    # 2. Ingest mock issues manually into KB
    documents = []
    for issue in mock_issues:
        content = jira_connector.format_issue(issue)
        doc = Document(
            page_content=content,
            metadata={"source": "jira", "key": issue["key"], "type": "requirement/bug"}
        )
        documents.append(doc)
    
    kb.add_documents(documents)
    print(f"Ingested {len(documents)} mock Jira issues into Knowledge Base.")
    
    # 3. Test Lead Agent planning with these issues in context
    lead_agent = QALeadAgent()
    print("\nRequesting mission plan for: 'Test the login flow'")
    mission = await lead_agent.analyze_and_plan("Test the login flow")
    
    print("\n--- Mission Plan ---")
    print(f"Priority: {mission.priority}")
    print(f"Risk Score: {mission.risk_score}")
    print(f"Target Agents: {mission.target_agents}")
    print("Objectives:")
    for obj in mission.objectives:
        print(f"  - {obj}")
        
    # Check if Jira context influenced the objectives
    found_jira_ref = any("QA-101" in obj or "mobile" in obj.lower() or "MFA" in obj or "QA-102" in obj for obj in mission.objectives)
    if found_jira_ref:
        print("\nSUCCESS: Jira context influenced the mission plan!")
    else:
        print("\nNOTE: Jira context might not have been cited, but check the objectives for mobile or MFA logic.")

if __name__ == "__main__":
    asyncio.run(verify_jira_rag())
