from .skill import Skill, SkillResult
from .shell_skill import ShellSkill

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("ToolRegistry")

# Keeping ToolResult for backward compatibility or refactoring it to SkillResult
ToolResult = SkillResult 

class ToolRegistry:
    """Central registry for tools and skills that agents can execute."""
    
    def __init__(self):
        self._skills: Dict[str, Skill] = {}
        self._setup_default_skills()

    def register_skill(self, skill: Skill):
        self._skills[skill.name] = skill
        logger.info(f"Registered skill: {skill.name}")

    def get_skill(self, name: str) -> Optional[Skill]:
        return self._skills.get(name)

    def list_skills(self) -> List[Dict[str, str]]:
        return [{"name": s.name, "description": s.description} for s in self._skills.values()]

    async def execute(self, skill_name: str, **kwargs) -> SkillResult:
        """Executes a skill by name with provided arguments."""
        skill = self.get_skill(skill_name)
        if not skill:
            return SkillResult(success=False, output="", error=f"Skill '{skill_name}' not found.")
        
        try:
            logger.info(f"Executing skill: {skill_name} with args: {kwargs}")
            return await skill.run(**kwargs)
        except Exception as e:
            logger.error(f"Error executing skill {skill_name}: {e}")
            return SkillResult(success=False, output="", error=str(e))

    def _setup_default_skills(self):
        """Registers some basic system skills."""
        self.register_skill(ShellSkill())

# Singleton instance
registry = ToolRegistry()
