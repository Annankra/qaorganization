from abc import ABC, abstractmethod
from typing import Any, Dict, Optional
from pydantic import BaseModel, Field

class SkillResult(BaseModel):
    success: bool
    output: Any
    error: Optional[str] = None
    metadata: Dict[str, Any] = Field(default_factory=dict)

class Skill(ABC):
    """Abstract base class for all agent skills."""
    
    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description

    @abstractmethod
    async def run(self, **kwargs) -> SkillResult:
        """Executes the skill logic."""
        pass

    def __repr__(self):
        return f"<Skill name='{self.name}'>"
