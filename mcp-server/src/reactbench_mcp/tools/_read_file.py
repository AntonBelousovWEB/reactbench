"""reactbench_read_task_file — read auxiliary file."""
from typing import Any
from .contracts import AppContext, ReadTaskFileInput


async def read_task_file(ctx: AppContext, inp: ReadTaskFileInput) -> dict[str, Any]:
    content = await ctx.tasks.read_aux_file(inp.task_id, inp.category, inp.filename)
    return {"task_id": inp.task_id, "category": inp.category, "filename": inp.filename, "content": content}
