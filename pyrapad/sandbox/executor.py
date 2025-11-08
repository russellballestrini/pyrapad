"""Docker-based code execution engine"""
import time
import tempfile
from pathlib import Path
from typing import Dict, Optional
from pyrapad.sandbox import ExecutionResult


# Language configurations
LANGUAGE_CONFIGS = {
    'python': {
        'image': 'python:3.11-alpine',
        'command': ['python', '-c'],
        'file_ext': '.py'
    },
    'javascript': {
        'image': 'node:20-alpine',
        'command': ['node', '-e'],
        'file_ext': '.js'
    },
    'ruby': {
        'image': 'ruby:3-alpine',
        'command': ['ruby', '-e'],
        'file_ext': '.rb'
    },
    'bash': {
        'image': 'bash:5-alpine',
        'command': ['bash', '-c'],
        'file_ext': '.sh'
    },
}


class CodeExecutor:
    """Execute code in isolated Docker containers"""

    def __init__(self, timeout: int = 5, memory_limit: str = '128m', cpu_limit: float = 1.0):
        """
        Initialize code executor

        Args:
            timeout: Maximum execution time in seconds
            memory_limit: Memory limit (e.g., '128m', '1g')
            cpu_limit: CPU limit (fraction of CPU, e.g., 1.0 = 1 CPU)
        """
        self.timeout = timeout
        self.memory_limit = memory_limit
        self.cpu_limit = cpu_limit
        self._docker_client = None

    @property
    def docker_client(self):
        """Lazy load Docker client"""
        if self._docker_client is None:
            try:
                import docker
                self._docker_client = docker.from_env()
            except ImportError:
                raise ImportError("docker package is required for code execution. "
                                  "Install with: pip install pyrapad[sandbox]")
            except Exception as e:
                raise RuntimeError(f"Failed to connect to Docker: {e}")
        return self._docker_client

    def execute(self, code: str, language: str = 'python') -> ExecutionResult:
        """
        Execute code in isolated container

        Args:
            code: Source code to execute
            language: Programming language

        Returns:
            ExecutionResult with stdout, stderr, and execution metadata
        """
        if language not in LANGUAGE_CONFIGS:
            return ExecutionResult(
                stdout='',
                stderr=f"Unsupported language: {language}",
                exit_code=1,
                execution_time=0.0,
                timed_out=False,
                error=f"Language '{language}' not supported"
            )

        config = LANGUAGE_CONFIGS[language]
        start_time = time.time()

        try:
            # Run code in container
            container = self.docker_client.containers.run(
                image=config['image'],
                command=config['command'] + [code],
                detach=True,
                remove=True,
                network_disabled=True,  # No network access
                mem_limit=self.memory_limit,
                cpu_period=100000,
                cpu_quota=int(100000 * self.cpu_limit),
                read_only=True,  # Readonly root filesystem
                security_opt=['no-new-privileges'],  # Security hardening
                cap_drop=['ALL'],  # Drop all capabilities
            )

            # Wait for completion with timeout
            try:
                result = container.wait(timeout=self.timeout)
                exit_code = result['StatusCode']
                timed_out = False
            except Exception:
                # Timeout occurred
                container.kill()
                exit_code = 124  # Timeout exit code
                timed_out = True

            # Get logs
            stdout = container.logs(stdout=True, stderr=False).decode('utf-8', errors='replace')
            stderr = container.logs(stdout=False, stderr=True).decode('utf-8', errors='replace')

            execution_time = time.time() - start_time

            return ExecutionResult(
                stdout=stdout,
                stderr=stderr,
                exit_code=exit_code,
                execution_time=execution_time,
                timed_out=timed_out
            )

        except Exception as e:
            execution_time = time.time() - start_time
            return ExecutionResult(
                stdout='',
                stderr=str(e),
                exit_code=1,
                execution_time=execution_time,
                timed_out=False,
                error=f"Execution error: {e}"
            )

    def get_supported_languages(self) -> list[str]:
        """Get list of supported programming languages"""
        return list(LANGUAGE_CONFIGS.keys())
