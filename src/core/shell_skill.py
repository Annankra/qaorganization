import subprocess
from .skill import Skill, SkillResult

class ShellSkill(Skill):
    """A skill that runs a shell command."""
    
    def __init__(self):
        super().__init__(
            name="run_shell",
            description="Runs a shell command and returns output. Args: command (str)"
        )

    async def run(self, command: str) -> SkillResult:
        try:
            result = subprocess.run(
                command, 
                shell=True, 
                capture_output=True, 
                text=True, 
                check=False
            )
            return SkillResult(
                success=result.returncode == 0,
                output=result.stdout,
                error=result.stderr if result.returncode != 0 else None,
                metadata={"returncode": result.returncode}
            )
        except Exception as e:
            return SkillResult(success=False, output="", error=str(e))
