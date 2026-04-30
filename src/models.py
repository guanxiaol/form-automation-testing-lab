from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any


class TaskStatus(str, Enum):
    PENDING = "pending"
    RUNNING = "running"
    SUCCEEDED = "succeeded"
    FAILED = "failed"


class ErrorCategory(str, Enum):
    CONFIGURATION = "configuration"
    NAVIGATION = "navigation"
    SELECTOR = "selector"
    VALIDATION = "validation"
    VERIFICATION = "verification"
    UNKNOWN = "unknown"


@dataclass
class StepResult:
    name: str
    status: TaskStatus
    started_at: str
    finished_at: str | None = None
    error_category: ErrorCategory | None = None
    error_message: str | None = None

    @classmethod
    def start(cls, name: str) -> "StepResult":
        return cls(name=name, status=TaskStatus.RUNNING, started_at=utc_now())

    def succeed(self) -> None:
        self.status = TaskStatus.SUCCEEDED
        self.finished_at = utc_now()

    def fail(self, category: ErrorCategory, message: str) -> None:
        self.status = TaskStatus.FAILED
        self.error_category = category
        self.error_message = message
        self.finished_at = utc_now()


@dataclass
class AutomationResult:
    task_id: str
    status: TaskStatus = TaskStatus.PENDING
    started_at: str = field(default_factory=utc_now)
    finished_at: str | None = None
    steps: list[StepResult] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def mark_running(self) -> None:
        self.status = TaskStatus.RUNNING

    def mark_succeeded(self) -> None:
        self.status = TaskStatus.SUCCEEDED
        self.finished_at = utc_now()

    def mark_failed(self) -> None:
        self.status = TaskStatus.FAILED
        self.finished_at = utc_now()

    def to_safe_dict(self) -> dict[str, Any]:
        return {
            "task_id": self.task_id,
            "status": self.status.value,
            "started_at": self.started_at,
            "finished_at": self.finished_at,
            "steps": [
                {
                    "name": step.name,
                    "status": step.status.value,
                    "started_at": step.started_at,
                    "finished_at": step.finished_at,
                    "error_category": step.error_category.value if step.error_category else None,
                    "error_message": step.error_message,
                }
                for step in self.steps
            ],
            "metadata": self.metadata,
        }


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()
