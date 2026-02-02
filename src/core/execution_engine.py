import subprocess
import os
import tempfile
import logging
import asyncio
from typing import Dict, Any, Optional

logger = logging.getLogger("ExecutionEngine")

class ExecutionResult:
    def __init__(self, success: bool, stdout: str, stderr: str, exit_code: int):
        self.success = success
        self.stdout = stdout
        self.stderr = stderr
        self.exit_code = exit_code

class ExecutionEngine:
    """Handles the execution of generated test scripts."""

    @staticmethod
    async def run_script(code: str, file_extension: str, command_prefix: list[str]) -> ExecutionResult:
        """
        Saves code to a temporary file and runs it with the given command prefix.
        """
        with tempfile.NamedTemporaryFile(suffix=file_extension, mode='w', delete=False) as temp_file:
            temp_file.write(code)
            temp_path = temp_file.name

        try:
            full_command = command_prefix + [temp_path]
            logger.info(f"Executing command: {' '.join(full_command)}")
            
            process = await asyncio.create_subprocess_exec(
                *full_command,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            
            stdout, stderr = await process.communicate()
            
            stdout_str = stdout.decode().strip()
            stderr_str = stderr.decode().strip()
            exit_code = process.returncode
            
            success = exit_code == 0
            
            return ExecutionResult(
                success=success,
                stdout=stdout_str,
                stderr=stderr_str,
                exit_code=exit_code
            )
        except Exception as e:
            logger.error(f"Execution failed: {e}")
            return ExecutionResult(
                success=False,
                stdout="",
                stderr=str(e),
                exit_code=-1
            )
        finally:
            if os.path.exists(temp_path):
                os.remove(temp_path)

    @classmethod
    async def run_playwright(cls, code: str) -> ExecutionResult:
        """Executes a Playwright test script."""
        # For Playwright Python scripts, we usually run them with pytest or python directly
        # If it's a standalone script, python3 is fine. If it's a pytest style, we need pytest.
        # The prompt in playwright_automation_skill.py asks for a "functional Playwright (Python) test script".
        # Let's assume standalone for now, or use python -m pytest if it looks like pytest.
        return await cls.run_script(code, ".py", ["python3"])

    @classmethod
    async def run_k6(cls, code: str) -> ExecutionResult:
        """Executes a k6 performance test script."""
        # Check if k6 is installed first maybe?
        return await cls.run_script(code, ".js", ["k6", "run"])
