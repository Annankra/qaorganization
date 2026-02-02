import logging
from typing import List, Dict, Any
from pydantic import BaseModel

logger = logging.getLogger("PolicyEngine")

class Policy(BaseModel):
    name: str
    condition: str
    action: str
    priority: int = 1

class PolicyEngine:
    """Heuristic-based decision engine for Lead Agent."""
    
    def __init__(self):
        self.policies: List[Policy] = []
        self._load_default_policies()

    def add_policy(self, name: str, condition: str, action: str, priority: int = 1):
        self.policies.append(Policy(name=name, condition=condition, action=action, priority=priority))
        logger.info(f"Added policy: {name}")

    def evaluate(self, context: Dict[str, Any]) -> List[str]:
        """Evaluates context against policies and returns recommended actions."""
        recommendations = []
        # Sort policies by priority (higher first)
        sorted_policies = sorted(self.policies, key=lambda x: x.priority, reverse=True)
        
        for policy in sorted_policies:
            # Basic keyword-based evaluation for now
            # In a real system, this could be a small LLM call or a DSL evaluator
            if policy.condition.lower() in str(context).lower():
                recommendations.append(policy.action)
        
        return recommendations

    def _load_default_policies(self):
        """Initial set of QA policies."""
        self.add_policy(
            name="Security First",
            condition="authentication",
            action="Always trigger SecurityAgent for auth changes.",
            priority=10
        )
        self.add_policy(
            name="Performance Baseline",
            condition="api",
            action="Trigger PerformanceAgent for new API endpoints.",
            priority=5
        )
        self.add_policy(
            name="Critical Path UI",
            condition="ui",
            action="Ensure E2EAgent covers critical user journeys.",
            priority=8
        )
