"""HarborClient protocol."""
from typing import Protocol


class HarborResult:
    __slots__ = ("command", "returncode", "_stdout_full", "_stderr_full", "_max_out", "_max_err")

    def __init__(self, *, command, returncode, stdout, stderr, max_stdout, max_stderr):
        self.command = command
        self.returncode = returncode
        self._stdout_full = stdout
        self._stderr_full = stderr
        self._max_out = max_stdout
        self._max_err = max_stderr

    @property
    def stdout(self):
        s = self._stdout_full
        return s[-self._max_out:] if len(s) > self._max_out else s

    @property
    def stderr(self):
        s = self._stderr_full
        return s[-self._max_err:] if len(s) > self._max_err else s

    @property
    def success(self):
        return self.returncode == 0


class HarborClient(Protocol):
    async def run(self, task_paths, *, agent="oracle", model="", n_concurrent=1,
                  timeout_multiplier=None, job_name=None, extra_args=None, extra_env=None) -> HarborResult: ...
