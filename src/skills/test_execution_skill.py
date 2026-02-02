from ..core.skill import Skill, SkillResult
from ..core.execution_engine import ExecutionEngine
import logging

logger = logging.getLogger("TestExecutionSkill")

class TestExecutionSkill(Skill):
    """A skill that executes generated test scripts using the ExecutionEngine."""
    
    def __init__(self):
        super().__init__(
            name="execute_test",
            description="Executes a generated test script. Args: code (str), test_type (str: 'playwright' or 'k6')"
        )

    async def run(self, code: str, test_type: str) -> SkillResult:
        try:
            # Clean up code block if present
            if "```python" in code:
                code = code.split("```python")[1].split("```")[0].strip()
            elif "```javascript" in code:
                code = code.split("```javascript")[1].split("```")[0].strip()
            elif "```" in code:
                code = code.split("```")[1].split("```")[0].strip()

            if test_type.lower() == "playwright":
                result = await ExecutionEngine.run_playwright(code)
            elif test_type.lower() == "k6":
                result = await ExecutionEngine.run_k6(code)
            else:
                return SkillResult(
                    success=False, 
                    output="", 
                    error=f"Unsupported test type: {test_type}"
                )

            output = f"Stdout:\n{result.stdout}\n\nStderr:\n{result.stderr}"
            
            # Truncate if too large to avoid token limit issues
            if len(output) > 5000:
                output = output[:5000] + "\n... [Output Truncated] ..."

            return SkillResult(
                success=result.success,
                output=output,
                metadata={
                    "test_type": test_type,
                    "exit_code": result.exit_code,
                    "success": result.success
                }
            )
        except Exception as e:
            logger.error(f"Error in TestExecutionSkill: {e}")
            return SkillResult(success=False, output="", error=str(e))
