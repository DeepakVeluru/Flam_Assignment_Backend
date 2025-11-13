"""
Job executor - runs jobs and handles output
"""

import subprocess
import shlex
from datetime import datetime, timedelta
from src.core.models import Job, JobState
from src.core.config import config


class JobExecutor:
    """Executes jobs and manages retry logic"""

    def __init__(self):
        self.timeout = config.get('worker_timeout', 3600)

    def execute(self, job: Job) -> tuple[bool, str, str]:
        """
        Execute a job
        Returns: (success: bool, output: str, error: str)
        """
        try:
            # Parse command - support both simple strings and complex shell commands
            if isinstance(job.command, str):
                # Use shell=True to support pipes, redirects, etc.
                result = subprocess.run(
                    job.command,
                    shell=True,
                    capture_output=True,
                    text=True,
                    timeout=self.timeout
                )
            else:
                return False, "", "Invalid command format"

            # Check return code
            if result.returncode == 0:
                return True, result.stdout, ""
            else:
                error = result.stderr if result.stderr else f"Command failed with exit code {result.returncode}"
                return False, result.stdout, error

        except subprocess.TimeoutExpired:
            return False, "", f"Command timed out after {self.timeout} seconds"
        except Exception as e:
            return False, "", str(e)

    def calculate_backoff(self, job: Job) -> datetime:
        """Calculate next retry time using exponential backoff"""
        backoff_base = config.get('backoff_base', 2)
        delay_seconds = backoff_base ** job.attempts
        return datetime.utcnow() + timedelta(seconds=delay_seconds)
