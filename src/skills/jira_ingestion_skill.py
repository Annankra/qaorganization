from ..core.skill import Skill, SkillResult
from ..core.jira_connector import jira_connector
from ..core.knowledge_base import kb
from langchain_core.documents import Document
import logging

logger = logging.getLogger("JiraIngestionSkill")

class JiraIngestionSkill(Skill):
    """A skill that fetches issues from Jira and ingests them into the Knowledge Base."""
    
    def __init__(self):
        super().__init__(
            name="ingest_jira_issues",
            description="Fetches Jira issues based on a JQL query and indexes them for RAG. Args: jql (str), limit (int, optional)"
        )

    async def run(self, jql: str, limit: int = 20) -> SkillResult:
        try:
            issues = jira_connector.fetch_issues(jql, limit=limit)
            if not issues:
                return SkillResult(
                    success=True,
                    output=f"No issues found for JQL: {jql}",
                    metadata={"count": 0}
                )
            
            documents = []
            for issue in issues:
                content = jira_connector.format_issue(issue)
                doc = Document(
                    page_content=content,
                    metadata={
                        "source": "jira",
                        "key": issue.get("key"),
                        "type": "requirement/bug"
                    }
                )
                documents.append(doc)
            
            kb.add_documents(documents)
            
            return SkillResult(
                success=True,
                output=f"Successfully ingested {len(documents)} issues from Jira.",
                metadata={"count": len(documents), "keys": [i.get("key") for i in issues]}
            )
        except Exception as e:
            logger.error(f"Error in JiraIngestionSkill: {e}")
            return SkillResult(success=False, output="", error=str(e))
