"""file — read auxiliary file."""
from ...tools.contracts import AppContext


async def run(ctx: AppContext, args: list[str]) -> None:
    if len(args) < 3:
        return print("Usage: file <task_id> <category> <filename>")
    print(await ctx.tasks.read_aux_file(args[0], args[1], args[2]))
