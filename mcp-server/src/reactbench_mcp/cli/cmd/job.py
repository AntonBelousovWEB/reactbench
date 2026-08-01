"""job — detailed result with patches."""
import json
from ...presentation.dto import job_to_detail
from ...tools.contracts import AppContext


async def run(ctx: AppContext, args: list[str]) -> None:
    if not args:
        return print("Usage: job <job_name>")
    job = await ctx.jobs.get(args[0])
    patches = {t.name: await ctx.jobs.read_trial_artifact(args[0], t.name, "patch") for t in job.trials}
    print(json.dumps(job_to_detail(job, patches=patches), indent=2, ensure_ascii=False))
