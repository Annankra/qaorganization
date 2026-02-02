import json
import os
import logging
from typing import List, Dict, Any
from pydantic import BaseModel

logger = logging.getLogger("MemoryManager")

class MemoryEntry(BaseModel):
    role: str
    content: str
    metadata: Dict[str, Any] = {}

class MemoryManager:
    """Handles persistence and retrieval of agent memory."""
    
    def __init__(self, agent_name: str, storage_dir: str = "data/memory"):
        self.agent_name = agent_name
        self.storage_dir = storage_dir
        self.file_path = os.path.join(storage_dir, f"{agent_name}_memory.json")
        self._ensure_storage()
        self.memory: List[MemoryEntry] = self._load_memory()

    def _ensure_storage(self):
        if not os.path.exists(self.storage_dir):
            os.makedirs(self.storage_dir)

    def _load_memory(self) -> List[MemoryEntry]:
        if os.path.exists(self.file_path):
            try:
                with open(self.file_path, "r") as f:
                    data = json.load(f)
                    return [MemoryEntry(**entry) for entry in data]
            except Exception as e:
                logger.error(f"Error loading memory for {self.agent_name}: {e}")
        return []

    def save_memory(self):
        try:
            with open(self.file_path, "w") as f:
                json.dump([entry.dict() for entry in self.memory], f, indent=2)
        except Exception as e:
            logger.error(f"Error saving memory for {self.agent_name}: {e}")

    def add_entry(self, role: str, content: str, metadata: Dict[str, Any] = None):
        # Aggressive truncation to prevent token bloom in agent history
        max_chars = 2000
        safe_content = content
        if len(content) > max_chars:
            safe_content = content[:max_chars] + "\n... [Memory Entry Truncated] ..."
            
        entry = MemoryEntry(role=role, content=safe_content, metadata=metadata or {})
        self.memory.append(entry)
        self.save_memory()

    def get_recent_context(self, limit: int = 10) -> List[MemoryEntry]:
        return self.memory[-limit:]

    def clear_memory(self):
        self.memory = []
        if os.path.exists(self.file_path):
            os.remove(self.file_path)
        logger.info(f"Cleared memory for {self.agent_name}")
