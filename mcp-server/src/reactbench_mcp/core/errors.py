"""Typed exception hierarchy."""


class ReactBenchError(Exception):
    """Base for all ReactBench MCP errors."""


class ConfigError(ReactBenchError):
    """Invalid configuration."""


class TaskNotFoundError(ReactBenchError):
    def __init__(self, task_id: str) -> None:
        super().__init__(f"Task not found: {task_id!r}")
        self.task_id = task_id


class TaskFileAccessError(ReactBenchError):
    def __init__(self, *, task_id: str, category: str, filename: str, reason: str) -> None:
        super().__init__(f"Cannot access {task_id!r}/{category}/{filename}: {reason}")
        self.task_id = task_id
        self.category = category
        self.filename = filename


class TaskFileNotFoundError(TaskFileAccessError):
    def __init__(self, *, task_id: str, category: str, filename: str) -> None:
        super().__init__(task_id=task_id, category=category, filename=filename, reason="File not found")


class JobNotFoundError(ReactBenchError):
    def __init__(self, job_name: str) -> None:
        super().__init__(f"Job not found: {job_name!r}")
        self.job_name = job_name


class HarborExecutionError(ReactBenchError):
    def __init__(self, command: list[str], returncode: int, stderr: str) -> None:
        super().__init__(f"Harbor exited with {returncode}: {' '.join(command)}")
        self.command = command
        self.returncode = returncode
        self.stderr = stderr
