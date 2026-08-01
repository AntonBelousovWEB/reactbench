"""verify — instruction + hidden tests."""
import json
from ...tools.contracts import AppContext


async def run(ctx: AppContext, args: list[str]) -> None:
    if not args:
        return print("Usage: verify <task_id>")
    task = await ctx.tasks.get(args[0])
    instruction = await ctx.tasks.read_instruction(args[0])
    test_files = {}
    for fname in task.file_tree().get("tests", ()):
        if fname.endswith((".spec.tsx", ".spec.ts", ".test.tsx", ".test.ts")):
            try:
                test_files[fname] = await ctx.tasks.read_aux_file(args[0], "tests", fname)
            except Exception:
                pass
    print(json.dumps({"task_id": args[0], "instruction": instruction, "test_files": test_files}, indent=2, ensure_ascii=False))
