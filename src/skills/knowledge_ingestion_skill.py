from ..core.skill import Skill, SkillResult
from ..core.knowledge_base import kb
from langchain_core.documents import Document
import logging

logger = logging.getLogger("KnowledgeIngestionSkill")

class KnowledgeIngestionSkill(Skill):
    """A skill that saves mission outcomes back to the Knowledge Base."""
    
    def __init__(self):
        super().__init__(
            name="ingest_outcome",
            description="Saves a mission's outcome, reports, and evaluation to the permanent knowledge base. Args: mission_id (str), content (str)"
        )

    async def run(self, mission_id: str, content: str) -> SkillResult:
        try:
            doc = Document(page_content=content, metadata={"mission_id": mission_id, "type": "mission_outcome"})
            kb.add_documents([doc])
            logger.info(f"Ingested mission outcome for {mission_id}")
            return SkillResult(
                success=True,
                output=f"Successfully ingested outcome for mission {mission_id}.",
                metadata={"mission_id": mission_id}
            )
        except Exception as e:
            logger.error(f"Error in KnowledgeIngestionSkill: {e}")
            return SkillResult(success=False, output="", error=str(e))
