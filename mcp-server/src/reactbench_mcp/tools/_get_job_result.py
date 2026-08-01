"""reactbench_get_job_result — detailed job with patches."""
from typing import Any
from ..presentation.dto import job_to_detail
from .contracts import AppContext, GetJobResultInput


async def get_job_result(ctx: AppContext, inp: GetJobResultInput) -> dict[str, Any]:
    job = await ctx.jobs.get(inp.job_name)
    patches = {
        t.name: await ctx.jobs.read_trial_artifact(inp.job_name, t.name, "patch")
        for t in job.trials
    }
    return job_to_detail(job, patches=patches)
