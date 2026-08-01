"""reactbench_list_tasks — discover tasks with filters."""
from typing import Any
from ..core.filtering import TaskFilter
from ..presentation.dto import task_to_summary
from .contracts import AppContext, ListTasksInput


async def list_tasks(ctx: AppContext, inp: ListTasksInput) -> dict[str, Any]:
    all_tasks = await ctx.tasks.list_all()
    filt = TaskFilter(
        difficulty=inp.difficulty, category=inp.category,
        tags=tuple(inp.tags) if inp.tags else None, name_glob=inp.name_glob,
    )
    filtered = filt.apply(iter(all_tasks))
    return {"n": len(filtered), "tasks": [task_to_summary(t) for t in filtered]}
