"""Code sandbox execution engine for pyrapad

This module provides secure code execution in isolated Docker containers.
"""
from dataclasses import dataclass
from typing import Optional
from datetime import datetime


@dataclass
class ExecutionResult:
    """Result of code execution in sandbox"""
    stdout: str
    stderr: str
    exit_code: int
    execution_time: float  # seconds
    timed_out: bool
    error: Optional[str] = None

    @property
    def success(self) -> bool:
        """Whether execution was successful"""
        return self.exit_code == 0 and not self.error and not self.timed_out

    def __repr__(self) -> str:
        status = "SUCCESS" if self.success else "FAILED"
        return f"<ExecutionResult status={status} exit_code={self.exit_code} time={self.execution_time:.2f}s>"
