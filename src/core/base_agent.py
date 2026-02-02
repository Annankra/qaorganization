from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage
import logging
import os
from .tool_registry import registry, ToolResult
from .memory_manager import MemoryManager, MemoryEntry
from .feedback_loop import FeedbackLoop

logger = logging.getLogger("BaseAgent")

class AgentMessage(BaseModel):
    role: str
    content: str

class BaseAgent:
    """Base class for all agents in the QA organization."""
    
    def __init__(
        self, 
        name: str, 
        role_description: str, 
        model_name: Optional[str] = None,
        temperature: Optional[float] = None,
        memory_dir: Optional[str] = None
    ):
        self.name = name
        self.role_description = role_description
        
        # Load from env or use defaults
        model = model_name or os.getenv("LLM_MODEL", "gpt-4o")
        temp = temperature if temperature is not None else float(os.getenv("TEMPERATURE", "0.7"))
        mem_dir = memory_dir or os.getenv("MEMORY_DIR", "data/memory")
        
        self.llm = ChatOpenAI(model=model, temperature=temp)
        self.memory_manager = MemoryManager(agent_name=name, storage_dir=mem_dir)
        self.feedback_loop = FeedbackLoop(self.memory_manager)
        self.tools = registry

    def add_to_memory(self, role: str, content: str):
        self.memory_manager.add_entry(role=role, content=content)

    def get_system_prompt(self) -> str:
        return f"""
        You are {self.name}.
        Role: {self.role_description}
        
        Use the tools available to you to complete your tasks.
        Focus on providing high-quality, actionable QA insights.
        """

    async def chat(self, user_input: str) -> str:
        """Simple chat interface for the agent."""
        messages = [SystemMessage(content=self.get_system_prompt())]
        
        # Add memory context
        for msg in self.memory_manager.get_recent_context(limit=10):
            if msg.role == "user":
                messages.append(HumanMessage(content=msg.content))
            else:
                messages.append(SystemMessage(content=msg.content))
        
        messages.append(HumanMessage(content=user_input))
        
        response = await self.llm.ainvoke(messages)
        content = response.content
        
        self.add_to_memory("user", user_input)
        self.add_to_memory("assistant", content)
        
        return content

    async def execute_tool(self, tool_name: str, **kwargs) -> ToolResult:
        return await self.tools.execute(tool_name, **kwargs)

    def __repr__(self):
        return f"<{self.__class__.__name__} name='{self.name}'>"
