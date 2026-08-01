"""CLI dispatcher — routes subcommand name to handler module."""
from __future__ import annotations
from typing import Callable, Awaitable
from ..tools.contracts import AppContext

Handler = Callable[[AppContext, list[str]], Awaitable[None]]

COMMANDS = {
    "tasks": ".cli.cmd.tasks", "task": ".cli.cmd.task", "verify": ".cli.cmd.verify",
    "file": ".cli.cmd.file", "jobs": ".cli.cmd.jobs", "job": ".cli.cmd.job",
    "check": ".cli.cmd.check", "--check": ".cli.cmd.check",
}


def run_cli(command: str, args: list[str]) -> None:
    import asyncio, importlib, sys
    from ..app import wire

    module_name = COMMANDS.get(command)
    if module_name is None:
        print(f"Unknown command: {command}", file=sys.stderr)
        print("Available: " + ", ".join(sorted(COMMANDS)), file=sys.stderr)
        sys.exit(1)

    try:
        mod = importlib.import_module(module_name, package="reactbench_mcp")
    except ImportError as exc:
        print(f"Command module not found: {module_name} ({exc})", file=sys.stderr)
        sys.exit(1)

    handler: Handler = getattr(mod, "run")
    asyncio.run(handler(wire(), args))
