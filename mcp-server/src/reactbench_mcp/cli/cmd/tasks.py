"""tasks — list with filters."""
import json
from ...core.filtering import TaskFilter
from ...presentation.dto import task_to_summary
from ...tools.contracts import AppContext


def _parse_filters(args):
    difficulty = None; tags = None; glob_pat = None; i = 0
    while i < len(args):
        if args[i] == "--difficulty" and i + 1 < len(args):
            difficulty = args[i + 1]; i += 2
        elif args[i] == "--tags" and i + 1 < len(args):
            tags = tuple(args[i + 1].split(",")); i += 2
        elif args[i] == "--glob" and i + 1 < len(args):
            glob_pat = args[i + 1]; i += 2
        else:
            i += 1
    return TaskFilter(difficulty=difficulty, tags=tags, name_glob=glob_pat)


async def run(ctx: AppContext, args: list[str]) -> None:
    filt = _parse_filters(args)
    all_tasks = await ctx.tasks.list_all()
    filtered = filt.apply(iter(all_tasks))
    print(json.dumps([task_to_summary(t) for t in filtered], indent=2, ensure_ascii=False))
