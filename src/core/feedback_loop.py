import logging
from typing import Dict, Any
from .memory_manager import MemoryManager

logger = logging.getLogger("FeedbackLoop")

class FeedbackLoop:
    """System to ingest and persist human feedback for agents."""
    
    def __init__(self, memory_manager: MemoryManager):
        self.memory_manager = memory_manager

    async def ingest_feedback(self, agent_name: str, feedback: str, context: Dict[str, Any]):
        """Saves human feedback to an agent's long-term memory."""
        content = f"HUMAN_FEEDBACK for {agent_name}: {feedback}\nContext: {context}"
        
        # Store in long-term memory (simulated as episodic/preference memory)
        # In a real RAG system, this would be an embedding-based store
        await self.memory_manager.store_memory(
            agent_name=agent_name,
            content=content,
            is_long_term=True
        )
        logger.info(f"Ingested human feedback for agent {agent_name}")

    async def get_agent_preferences(self, agent_name: str) -> str:
        """Retrieves historical feedback for an agent to guide its behavior."""
        memories = await self.memory_manager.get_memories(agent_name, limit=5)
        feedback_memories = [m for m in memories if "HUMAN_FEEDBACK" in m]
        return "\n".join(feedback_memories) if feedback_memories else "No specific human feedback yet."
