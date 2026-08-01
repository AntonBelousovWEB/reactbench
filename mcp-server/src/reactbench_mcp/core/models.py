"""Pure frozen domain models."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

from .errors import TaskFileAccessError


@dataclass(frozen=True)
class TaskMetadata:
    difficulty: str
    category: str
    tags: tuple[str, ...] = ()
    origin: str | None = None
    base_sha: str | None = None


@dataclass(frozen=True)
class TaskLimits:
    agent_timeout_sec: float = 900.0
    verifier_timeout_sec: float = 300.0
    cpus: int = 1
    memory_mb: int = 2048
    storage_mb: int = 10240


@dataclass(frozen=True)
class Task:
    id: str
    path: Path
    metadata: TaskMetadata
    limits: TaskLimits
    version: str = "1.0"

    _KNOWN_CATEGORIES: tuple[str, ...] = ("tests", "solution", "environment")

    @property
    def instruction_path(self) -> Path:
        return self.path / "instruction.md"

    def category_dir(self, category: str) -> Path:
        if category not in self._KNOWN_CATEGORIES:
            raise TaskFileAccessError(
                task_id=self.id, category=category, filename="",
                reason=f"Unknown category (expected one of {self._KNOWN_CATEGORIES})",
            )
        return self.path / category

    def resolve_aux_file(self, category: str, filename: str) -> Path:
        if category not in self._KNOWN_CATEGORIES:
            raise TaskFileAccessError(
                task_id=self.id, category=category, filename=filename,
                reason="Unknown category",
            )
        base = self.category_dir(category).resolve()
        resolved = (base / filename).resolve()
        if not str(resolved).startswith(str(base)):
            raise TaskFileAccessError(
                task_id=self.id, category=category, filename=filename,
                reason="Path traversal detected",
            )
        return resolved

    def file_tree(self) -> dict[str, tuple[str, ...]]:
        tree: dict[str, tuple[str, ...]] = {}
        for cat in self._KNOWN_CATEGORIES:
            d = self.category_dir(cat)
            if d.is_dir():
                tree[cat] = tuple(
                    sorted(str(f.relative_to(d)) for f in d.rglob("*") if f.is_file())
                )
        return tree


@dataclass(frozen=True)
class TrialReward:
    raw: str
    detail: dict | None = None


@dataclass(frozen=True)
class Trial:
    name: str
    reward: TrialReward | None = None
    changed_files: tuple[str, ...] = ()
    has_artifacts: bool = False


@dataclass(frozen=True)
class Job:
    name: str
    trials: tuple[Trial, ...] = ()

    @property
    def trial_count(self) -> int:
        return len(self.trials)
