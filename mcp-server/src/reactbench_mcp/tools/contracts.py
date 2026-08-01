"""Typed input models + AppContext DI container."""
from dataclasses import dataclass, field
from typing import Any, Protocol
from ..config import AppConfig
from ..ports.harbor import HarborClient
from ..ports.job_store import JobStore
from ..ports.task_store import TaskStore


@dataclass(frozen=True)
class AppContext:
    config: AppConfig
    tasks: TaskStore
    jobs: JobStore
    harbor: HarborClient


@dataclass(frozen=True)
class ListTasksInput:
    difficulty: str | None = None
    category: str | None = None
    tags: list[str] | None = None
    name_glob: str | None = None


@dataclass(frozen=True)
class GetTaskInput:
    task_id: str


@dataclass(frozen=True)
class ReadTaskFileInput:
    task_id: str
    category: str
    filename: str


@dataclass(frozen=True)
class RunTasksInput:
    task_paths: list[str] = field(default_factory=lambda: ["tasks"])
    agent: str = "oracle"
    model: str = ""
    n_concurrent: int = 1
    timeout_multiplier: float | None = None
    job_name: str | None = None
    env: dict[str, str] | None = None
    extra_args: list[str] | None = None


@dataclass(frozen=True)
class ListJobsInput:
    pass


@dataclass(frozen=True)
class GetJobResultInput:
    job_name: str


class ToolHandler(Protocol):
    async def __call__(self, ctx: AppContext, inp: Any) -> dict[str, Any]: ...
