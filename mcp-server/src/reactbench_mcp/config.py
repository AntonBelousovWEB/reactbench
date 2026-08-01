"""Validated, frozen AppConfig."""
import os
from dataclasses import dataclass, field
from pathlib import Path

_HARBOR_RUN_TIMEOUT = 7200.0
_MAX_STDOUT = 20_000
_MAX_STDERR = 10_000
_MAX_PATCH = 30_000
_MAX_LOG = 10_000


def _find_repo_root() -> Path:
    env = os.environ.get("REACTBENCH_ROOT")
    if env:
        c = Path(env).expanduser().resolve()
        if (c / "tasks").is_dir() and (c / "pyproject.toml").is_file():
            return c
    here = Path(__file__).resolve()
    for levels in (4, 3):
        root = here
        for _ in range(levels):
            root = root.parent
        if (root / "tasks").is_dir() and (root / "pyproject.toml").is_file():
            return root
    cwd = Path.cwd()
    if (cwd / "tasks").is_dir() and (cwd / "pyproject.toml").is_file():
        return cwd
    raise FileNotFoundError("Cannot locate ReactBench root. Set REACTBENCH_ROOT.")


@dataclass(frozen=True)
class AppConfig:
    repo_root: Path = field(default_factory=_find_repo_root)
    harbor_bin: tuple[str, ...] = ("uv", "run", "harbor")
    harbor_run_timeout_sec: float = _HARBOR_RUN_TIMEOUT
    harbor_read_timeout_sec: float = 10.0
    max_stdout_bytes: int = _MAX_STDOUT
    max_stderr_bytes: int = _MAX_STDERR
    max_patch_bytes: int = _MAX_PATCH
    max_log_bytes: int = _MAX_LOG

    @property
    def tasks_dir(self) -> Path:
        return self.repo_root / "tasks"

    @property
    def jobs_dir(self) -> Path:
        return self.repo_root / "jobs"

    def __post_init__(self) -> None:
        if not self.repo_root.exists():
            return
        if not self.tasks_dir.is_dir():
            raise FileNotFoundError(f"Tasks dir not found: {self.tasks_dir}")
