"""Tool dispatch table."""
from typing import Any
from ._get_job_result import get_job_result, GetJobResultInput
from ._get_task import get_task, GetTaskInput
from ._list_jobs import list_jobs, ListJobsInput
from ._list_tasks import list_tasks, ListTasksInput
from ._read_file import read_task_file, ReadTaskFileInput
from ._run import run_tasks, RunTasksInput
from ._verify import verify

TOOL_DISPATCH: dict[str, tuple[Any, type]] = {
    "reactbench_list_tasks": (list_tasks, ListTasksInput),
    "reactbench_get_task": (get_task, GetTaskInput),
    "reactbench_read_task_file": (read_task_file, ReadTaskFileInput),
    "reactbench_verify": (verify, GetTaskInput),
    "reactbench_run_tasks": (run_tasks, RunTasksInput),
    "reactbench_list_jobs": (list_jobs, ListJobsInput),
    "reactbench_get_job_result": (get_job_result, GetJobResultInput),
}
