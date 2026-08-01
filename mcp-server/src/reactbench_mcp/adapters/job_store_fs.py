"""Filesystem JobStore."""
import json
from pathlib import Path
from typing import final
from ..config import AppConfig
from ..core.errors import JobNotFoundError
from ..core.models import Job, Trial, TrialReward


@final
class FilesystemJobStore:
    __slots__ = ("_jobs_dir", "_max_patch", "_max_log")

    def __init__(self, config: AppConfig) -> None:
        self._jobs_dir = config.jobs_dir
        self._max_patch = config.max_patch_bytes
        self._max_log = config.max_log_bytes

    async def list_all(self) -> list[Job]:
        if not self._jobs_dir.is_dir():
            return []
        return [self._parse_job(d) for d in sorted(self._jobs_dir.iterdir()) if d.is_dir()]

    async def get(self, job_name: str) -> Job:
        jd = self._jobs_dir / job_name
        if not jd.is_dir():
            raise JobNotFoundError(job_name)
        return self._parse_job(jd)

    async def read_trial_artifact(self, job_name: str, trial_name: str, kind: str) -> str | None:
        td = self._jobs_dir / job_name / trial_name
        if not td.is_dir():
            return None
        if kind == "patch":
            p = td / "artifacts" / "agent.patch"
            return p.read_text()[:self._max_patch] if p.is_file() else None
        if kind == "diffstat":
            p = td / "artifacts" / "agent-diff-stat.txt"
            return p.read_text() if p.is_file() else None
        if kind.startswith("log_"):
            p = td / "logs" / kind[4:]
            return p.read_text()[:self._max_log] if p.is_file() else None
        return None

    def _parse_job(self, jd: Path) -> Job:
        return Job(name=jd.name, trials=tuple(self._parse_trials(jd)))

    def _parse_trials(self, jd: Path):
        for td in sorted(jd.iterdir()):
            if not td.is_dir():
                continue
            r = self._read_reward(td)
            cf = self._read_changed(td)
            yield Trial(name=td.name, reward=r, changed_files=tuple(cf), has_artifacts=(td / "artifacts").is_dir())

    @staticmethod
    def _read_reward(td: Path) -> TrialReward | None:
        vd = td / "verifier"
        txt = vd / "reward.txt"
        if not txt.is_file():
            return None
        detail = None
        jp = vd / "reward.json"
        if jp.is_file():
            try:
                detail = json.loads(jp.read_text())
            except json.JSONDecodeError:
                pass
        return TrialReward(raw=txt.read_text().strip(), detail=detail)

    @staticmethod
    def _read_changed(td: Path) -> list[str]:
        cf = td / "artifacts" / "changed-files.txt"
        return cf.read_text().strip().split("\n")[:20] if cf.is_file() else []
