"""task — full details."""
import json
from ...presentation.dto import task_to_detail
from ...tools.contracts import AppContext


async def run(ctx: AppContext, args: list[str]) -> None:
    if not args:
        return print("Usage: task <task_id>")
    task = await ctx.tasks.get(args[0])
    instruction = await ctx.tasks.read_instruction(args[0])
    print(json.dumps(task_to_detail(task, instruction=instruction), indent=2, ensure_ascii=False))
