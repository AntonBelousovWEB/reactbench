"""jobs — list past runs."""
import json
from ...presentation.dto import job_to_summary
from ...tools.contracts import AppContext


async def run(ctx: AppContext, args: list[str]) -> None:
    jobs = await ctx.jobs.list_all()
    if not jobs:
        return print("No jobs found.")
    for j in jobs:
        print(json.dumps(job_to_summary(j), indent=2, ensure_ascii=False))
