import os
import logging
from typing import List, Dict, Any, Optional
from atlassian import Jira

logger = logging.getLogger("JiraConnector")

class JiraConnector:
    """Connector for interacting with Jira API."""
    
    def __init__(self):
        self.url = os.getenv("JIRA_URL")
        self.username = os.getenv("JIRA_USER_EMAIL")
        self.api_token = os.getenv("JIRA_API_TOKEN")
        
        if not all([self.url, self.username, self.api_token]):
            logger.warning("Jira credentials not fully configured in environment. Jira integration will be limited.")
            self.client = None
        else:
            try:
                self.client = Jira(
                    url=self.url,
                    username=self.username,
                    password=self.api_token,
                    cloud=True
                )
                logger.info(f"Initialized Jira connector for {self.url}")
            except Exception as e:
                logger.error(f"Failed to initialize Jira client: {e}")
                self.client = None

    def fetch_issues(self, jql: str, limit: int = 50) -> List[Dict[str, Any]]:
        """Fetches issues from Jira using a JQL query."""
        if not self.client:
            logger.error("Jira client not initialized. Cannot fetch issues.")
            return []
            
        try:
            results = self.client.jql(jql, limit=limit)
            issues = results.get("issues", [])
            logger.info(f"Fetched {len(issues)} issues from Jira with JQL: {jql}")
            return issues
        except Exception as e:
            logger.error(f"Error fetching Jira issues: {e}")
            return []

    def format_issue(self, issue: Dict[str, Any]) -> str:
        """Formats a raw Jira issue into a readable string for RAG."""
        fields = issue.get("fields", {})
        key = issue.get("key")
        summary = fields.get("summary", "No Summary")
        description = fields.get("description", "No Description")
        status = fields.get("status", {}).get("name")
        issue_type = fields.get("issuetype", {}).get("name")
        priority = fields.get("priority", {}).get("name")
        
        # Handle complex description format if needed (Atlassian Document Format)
        if isinstance(description, dict):
            # Very basic extraction for ADF
            text_blocks = []
            for item in description.get("content", []):
                for sub_item in item.get("content", []):
                    if sub_item.get("type") == "text":
                        text_blocks.append(sub_item.get("text"))
            description = " ".join(text_blocks)
            
        return f"""
Jira Issue: {key}
Type: {issue_type}
Status: {status}
Priority: {priority}
Summary: {summary}
Description: {description}
"""

# Singleton instance
jira_connector = JiraConnector()
