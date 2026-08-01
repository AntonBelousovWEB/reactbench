"""DTO serializers — domain to JSON-safe dicts."""
from typing import Any
from ..core.models import Job, Task, Trial


def task_to_summary(task: Task) -> dict[str, Any]:
    return {
        "id": task.id, "diff": task.metadata.difficulty, "cat": task.metadata.category,
        "tags": list(task.metadata.tags), "origin": task.metadata.origin,
        "tout_agent": task.limits.agent_timeout_sec, "tout_verif": task.limits.verifier_timeout_sec,
    }


def task_to_detail(task: Task, *, instruction: str = "") -> dict[str, Any]:
    return {
        "id": task.id, "instruction": instruction, "diff": task.metadata.difficulty,
        "cat": task.metadata.category, "tags": list(task.metadata.tags), "origin": task.metadata.origin,
        "base_sha": task.metadata.base_sha, "tout_agent": task.limits.agent_timeout_sec,
        "tout_verif": task.limits.verifier_timeout_sec, "cpu": task.limits.cpus,
        "mem_mb": task.limits.memory_mb, "disk_mb": task.limits.storage_mb,
        "files": {cat: list(files) for cat, files in task.file_tree().items()},
    }


def trial_to_dict(trial: Trial) -> dict[str, Any]:
    d: dict[str, Any] = {"n": trial.name}
    if trial.reward is not None:
        d["r"] = trial.reward.raw
        if trial.reward.detail is not None:
            d["rd"] = trial.reward.detail
    if trial.changed_files:
        d["cf"] = list(trial.changed_files)
    d["art"] = trial.has_artifacts
    return d


def job_to_summary(job: Job) -> dict[str, Any]:
    return {"name": job.name, "n_trials": job.trial_count, "trials": [trial_to_dict(t) for t in job.trials]}


def job_to_detail(job: Job, *, patches=None, diffstats=None, logs=None) -> dict[str, Any]:
    result: dict[str, Any] = {"name": job.name, "n_trials": job.trial_count, "trials": []}
    for trial in job.trials:
        td = trial_to_dict(trial)
        name = trial.name
        if patches and name in patches:
            td["patch"] = patches[name]
        if diffstats and name in diffstats:
            td["diff"] = diffstats[name]
        if logs and name in logs:
            td["log"] = logs[name]
        result["trials"].append(td)
    return result
