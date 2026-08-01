"""MCP tool JSON schemas with agent directives."""
from typing import Any


def _obj(*, required=None, **props):
    s = {"type": "object", "properties": props}
    if required:
        s["required"] = required
    return s


def _str(description="", enum=None):
    s = {"type": "string", "description": description}
    if enum:
        s["enum"] = enum
    return s


def _arr(items, description=""):
    return {"type": "array", "items": items, "description": description}


def _int(description=""):
    return {"type": "integer", "description": description}


def _num(description=""):
    return {"type": "number", "description": description}


TOOL_SCHEMAS: dict[str, tuple[str, dict[str, Any]]] = {
    "reactbench_list_tasks": (
        "Call ONCE to discover tasks. Use filters to narrow down.",
        _obj(difficulty=_str(enum=["easy", "medium", "hard"]), category=_str(),
             tags=_arr(_str()), name_glob=_str()),
    ),
    "reactbench_get_task": (
        "Call ONCE per task. Prefer reactbench_verify for development.",
        _obj(required=["task_id"], task_id=_str()),
    ),
    "reactbench_read_task_file": (
        "Read a file from tests/solution/environment. Use verify instead.",
        _obj(required=["task_id", "category", "filename"], task_id=_str(),
             category=_str(enum=["tests", "solution", "environment"]), filename=_str()),
    ),
    "reactbench_verify": (
        "DEVELOPMENT VERIFICATION — call AFTER writing ALL code, before final grading. "
        "Batch your changes: write the COMPLETE solution, then call verify ONCE. "
        "For final grading use reactbench_run_tasks.",
        _obj(required=["task_id"], task_id=_str()),
    ),
    "reactbench_run_tasks": (
        "FINAL GRADING ONLY. Heavy: Docker+uv+API keys. Do NOT use for dev loops.",
        _obj(task_paths=_arr(_str()), agent=_str(), model=_str(), n_concurrent=_int(),
             timeout_multiplier=_num(), job_name=_str(), env=_obj(), extra_args=_arr(_str())),
    ),
    "reactbench_list_jobs": (
        "Check past evaluation results. Call after run_tasks.",
        _obj(),
    ),
    "reactbench_get_job_result": (
        "Inspect a completed job: rewards, patches, logs. Call after list_jobs.",
        _obj(required=["job_name"], job_name=_str()),
    ),
}
