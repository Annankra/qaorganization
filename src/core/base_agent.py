from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field
from langchain_openai import ChatOpenAI
from langchain.schema import SystemMessage, HumanMessage
import logging
from .tool_registry import registry, ToolResult

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
        model_name: str = "gpt-4o",
        temperature: float = 0.7
    ):
        self.name = name
        self.role_description = role_description
        self.llm = ChatOpenAI(model=model_name, temperature=temperature)
        self.memory: List[AgentMessage] = []
        self.tools = registry

    def add_to_memory(self, role: str, content: str):
        self.memory.append(AgentMessage(role=role, content=content))

    def get_system_prompt(self) -> str:
        return f"You are {self.name}, {self.role_description}. Use the tools available to you to complete your tasks."

    async def chat(self, user_input: str) -> str:
        """Simple chat interface for the agent."""
        messages = [SystemMessage(content=self.get_system_prompt())]
        
        # Add memory context
        for msg in self.memory[-10:]:  # Keep last 10 messages for context
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
