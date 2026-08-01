"""reactbench_verify — lightweight, no Docker."""
from typing import Any
from .contracts import AppContext, GetTaskInput


async def verify(ctx: AppContext, inp: GetTaskInput) -> dict[str, Any]:
    task = await ctx.tasks.get(inp.task_id)
    instruction = await ctx.tasks.read_instruction(inp.task_id)
    test_files: dict[str, str] = {}
    for fname in task.file_tree().get("tests", ()):
        if fname.endswith((".spec.tsx", ".spec.ts", ".test.tsx", ".test.ts")):
            try:
                test_files[fname] = await ctx.tasks.read_aux_file(inp.task_id, "tests", fname)
            except Exception:
                pass
    return {
        "task_id": inp.task_id, "instruction": instruction, "test_files": test_files,
        "hint": "Run locally: vitest/jest. For final grading use reactbench_run_tasks.",
    }
