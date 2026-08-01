"""check — validate config, discover tasks."""
from collections import Counter
from ...config import AppConfig
from ...adapters import FilesystemTaskStore
from ...tools.contracts import AppContext


async def run(ctx: AppContext, args: list[str]) -> None:
    print("ReactBench MCP server — configuration check\n")
    try:
        config = AppConfig()
        print(f"  ✅ Config OK — {config.repo_root}")
    except Exception as e:
        print(f"  ❌ Config FAILED: {e}")
        raise SystemExit(1)

    tasks = await FilesystemTaskStore(config).list_all()
    diffs = Counter(t.metadata.difficulty for t in tasks)
    cats = Counter(t.metadata.category for t in tasks)
    print(f"  ✅ Discovered {len(tasks)} tasks")
    print(f"     difficulty: {dict(diffs)}")
    print(f"     category:   {dict(cats)}")

    t = await FilesystemTaskStore(config).get("hello-react")
    instr = await FilesystemTaskStore(config).read_instruction("hello-react")
    print(f"  ✅ Read 'hello-react' — {len(instr)} chars")
    print("\n  ✅ All checks passed. Ready for MCP connections.")
