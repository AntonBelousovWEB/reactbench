"""Async subprocess Harbor client."""
import asyncio
import os
from typing import final
from ..config import AppConfig
from ..core.errors import HarborExecutionError
from ..ports.harbor import HarborResult


@final
class SubprocessHarborClient:
    __slots__ = ("_config",)

    def __init__(self, config: AppConfig) -> None:
        self._config = config

    async def run(self, task_paths, *, agent="oracle", model="", n_concurrent=1,
                  timeout_multiplier=None, job_name=None, extra_args=None, extra_env=None):
        cmd = list(self._config.harbor_bin) + ["run"]
        for p in task_paths:
            cmd.extend(("-p", p))
        if agent:
            cmd.extend(("-a", agent))
        if model:
            cmd.extend(("-m", model))
        cmd.extend(("-n", str(n_concurrent)))
        if timeout_multiplier is not None:
            cmd.extend(("--timeout-multiplier", str(timeout_multiplier)))
        if job_name:
            cmd.extend(("--job-name", job_name))
        if extra_args:
            cmd.extend(extra_args)
        env = {**os.environ, "PYTHONUNBUFFERED": "1"}
        if extra_env:
            env.update(extra_env)
        proc = await asyncio.create_subprocess_exec(
            *cmd, cwd=str(self._config.repo_root),
            stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE, env=env,
        )
        try:
            out, err = await asyncio.wait_for(proc.communicate(), timeout=self._config.harbor_run_timeout_sec)
        except asyncio.TimeoutError:
            proc.kill()
            await proc.wait()
            raise HarborExecutionError(cmd, -1, "Timed out")
        return HarborResult(
            command=cmd, returncode=proc.returncode or 0,
            stdout=out.decode("utf-8", errors="replace"),
            stderr=err.decode("utf-8", errors="replace"),
            max_stdout=self._config.max_stdout_bytes,
            max_stderr=self._config.max_stderr_bytes,
        )
