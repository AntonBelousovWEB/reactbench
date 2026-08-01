"""reactbench_run_tasks — execute Harbor evaluation."""
from typing import Any
from .contracts import AppContext, RunTasksInput


async def run_tasks(ctx: AppContext, inp: RunTasksInput) -> dict[str, Any]:
    result = await ctx.harbor.run(
        task_paths=inp.task_paths, agent=inp.agent, model=inp.model,
        n_concurrent=inp.n_concurrent, timeout_multiplier=inp.timeout_multiplier,
        job_name=inp.job_name, extra_args=inp.extra_args, extra_env=inp.env,
    )
    return {
        "command": " ".join(result.command), "returncode": result.returncode,
        "stdout": result.stdout, "stderr": result.stderr, "success": result.success,
    }
