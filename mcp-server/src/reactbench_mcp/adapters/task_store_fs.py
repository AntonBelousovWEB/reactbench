"""Filesystem TaskStore."""
import tomllib
from pathlib import Path
from typing import final
from ..config import AppConfig
from ..core.errors import TaskFileNotFoundError, TaskNotFoundError
from ..core.models import Task, TaskLimits, TaskMetadata


@final
class FilesystemTaskStore:
    __slots__ = ("_tasks_dir",)

    def __init__(self, config: AppConfig) -> None:
        self._tasks_dir = config.tasks_dir

    async def list_all(self) -> list[Task]:
        if not self._tasks_dir.is_dir():
            raise FileNotFoundError(f"Tasks dir not found: {self._tasks_dir}")
        tasks = []
        for entry in sorted(self._tasks_dir.iterdir()):
            if not entry.is_dir():
                continue
            tp = entry / "task.toml"
            if tp.is_file():
                tasks.append(self._parse(entry.name, entry, tp))
        return tasks

    async def get(self, task_id: str) -> Task:
        td = self._tasks_dir / task_id
        tp = td / "task.toml"
        if not td.is_dir() or not tp.is_file():
            raise TaskNotFoundError(task_id)
        return self._parse(task_id, td, tp)

    async def read_instruction(self, task_id: str) -> str:
        task = await self.get(task_id)
        ip = task.instruction_path
        if not ip.is_file():
            raise TaskFileNotFoundError(task_id=task_id, category="instruction", filename="instruction.md")
        return ip.read_text(encoding="utf-8")

    async def read_aux_file(self, task_id: str, category: str, filename: str) -> str:
        task = await self.get(task_id)
        r = task.resolve_aux_file(category, filename)
        if not r.is_file():
            raise TaskFileNotFoundError(task_id=task_id, category=category, filename=filename)
        return r.read_text(encoding="utf-8")

    @staticmethod
    def _parse(task_id: str, task_dir: Path, toml_path: Path) -> Task:
        with toml_path.open("rb") as fh:
            raw = tomllib.load(fh)
        meta = raw.get("metadata", {})
        env = raw.get("environment", {})
        ve = raw.get("verifier", {}).get("environment", {})
        ag = raw.get("agent", {})
        return Task(
            id=task_id, path=task_dir, version=raw.get("version", "1.0"),
            metadata=TaskMetadata(
                difficulty=meta.get("difficulty", "unknown"),
                category=meta.get("category", "unknown"),
                tags=tuple(meta.get("tags", ())),
                origin=meta.get("origin"),
                base_sha=meta.get("base_sha"),
            ),
            limits=TaskLimits(
                agent_timeout_sec=float(ag.get("timeout_sec", 900.0)),
                verifier_timeout_sec=float(raw.get("verifier", {}).get("timeout_sec", 300.0)),
                cpus=int(env.get("cpus", ve.get("cpus", 1))),
                memory_mb=int(env.get("memory_mb", ve.get("memory_mb", 2048))),
                storage_mb=int(env.get("storage_mb", ve.get("storage_mb", 10240))),
            ),
        )
