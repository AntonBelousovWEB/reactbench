"""reactbench_list_jobs — list past runs."""
from typing import Any
from ..presentation.dto import job_to_summary
from .contracts import AppContext, ListJobsInput


async def list_jobs(ctx: AppContext, _inp: ListJobsInput) -> dict[str, Any]:
    jobs = await ctx.jobs.list_all()
    if not jobs:
        return {"jobs": [], "message": "No jobs found. Run some tasks first."}
    return {"n": len(jobs), "jobs": [job_to_summary(j) for j in jobs]}
