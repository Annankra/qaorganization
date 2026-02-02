from .base_agent import BaseAgent
from typing import List, Dict, Any
from pydantic import BaseModel
import json

class EvaluationResult(BaseModel):
    score: int
    rationale: str
    feedback: List[str]

class EvalAgent(BaseAgent):
    """Specialist agent for evaluating the success and quality of QA missions."""
    
    def __init__(self, name: str = "QA_Evaluation_Specialist"):
        super().__init__(
            name=name,
            role_description="Expert in QA metrics and organizational effectiveness. Responsible for scoring mission outcomes."
        )

    async def evaluate_mission(self, state: Dict[str, Any]) -> EvaluationResult:
        """Scores the mission based on the state (input, mission, reports)."""
        reports_content = "\n\n".join(state.get("reports", []))
        input_data = state.get("input", "")
        mission = state.get("mission")
        
        prompt = f"""
        Evaluate the following QA mission.
        
        Original Input: {input_data}
        Target Agents: {mission.target_agents if mission else "Unknown"}
        
        Gathered Reports:
        {reports_content}
        
        Provide an evaluation in JSON format:
        {{
          "score": <int 1-10>,
          "rationale": "<brief explanation>",
          "feedback": ["<feedback point 1>", "<feedback point 2>"]
        }}
        """
        
        response = await self.chat(prompt)
        try:
            # Basic JSON extraction (in production, use a more robust parser)
            cleaned_response = response.strip()
            if "```json" in cleaned_response:
                cleaned_response = cleaned_response.split("```json")[1].split("```")[0].strip()
            
            data = json.loads(cleaned_response)
            return EvaluationResult(**data)
        except Exception:
            return EvaluationResult(score=5, rationale="Failed to parse eval", feedback=[response])

    def get_system_prompt(self) -> str:
        base_prompt = super().get_system_prompt()
        return base_prompt + "\nBe objective and rigorous. High scores should only be given for comprehensive and actionable QA outputs."
