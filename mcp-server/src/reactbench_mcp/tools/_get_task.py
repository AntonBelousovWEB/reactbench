"""reactbench_get_task — full task details."""
from typing import Any
from ..presentation.dto import task_to_detail
from .contracts import AppContext, GetTaskInput


async def get_task(ctx: AppContext, inp: GetTaskInput) -> dict[str, Any]:
    task = await ctx.tasks.get(inp.task_id)
    instruction = await ctx.tasks.read_instruction(inp.task_id)
    return task_to_detail(task, instruction=instruction)
