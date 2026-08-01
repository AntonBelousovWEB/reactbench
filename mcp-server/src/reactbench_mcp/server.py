"""MCP stdio transport — thin layer, zero business logic."""
import json
import logging
from typing import Any

import anyio
import mcp_types as types
from mcp.server.lowlevel import Server
from mcp.server.stdio import stdio_server

from .core.errors import ReactBenchError
from .presentation.schemas import TOOL_SCHEMAS
from .tools.contracts import AppContext
from .tools.registry import TOOL_DISPATCH

_log = logging.getLogger("reactbench-mcp.transport")


def _build_server(ctx: AppContext) -> Server:
    async def on_list_tools(_sc: Any, _params: Any) -> types.ListToolsResult:
        tools = [
            {"name": n, "description": d, "inputSchema": s}
            for n, (d, s) in TOOL_SCHEMAS.items()
        ]
        return types.ListToolsResult(tools=tools)

    async def on_call_tool(
        _sc: Any, params: types.CallToolRequestParams
    ) -> types.CallToolResult:
        name = params.name
        arguments: dict[str, Any] = params.arguments or {}

        entry = TOOL_DISPATCH.get(name)
        if entry is None:
            return _err(f"Unknown tool: {name}")

        handler, input_cls = entry
        try:
            fields = input_cls.__dataclass_fields__
            kw = {k: arguments[k] for k in fields if k in arguments}
            inp = input_cls(**kw)
            result = await handler(ctx, inp)
            return _ok(result)
        except ReactBenchError as exc:
            _log.warning("Tool %s rejected: %s", name, exc)
            return _err(str(exc))
        except Exception:
            _log.exception("Unexpected error in tool %s", name)
            return _err(f"Internal error in {name}")

    return Server(
        name="reactbench",
        version="0.3.0",
        title="ReactBench MCP Server",
        description=(
            "MCP server for ReactBench — evaluating coding agents on realistic "
            "React work. List tasks, inspect instructions, run evaluations, "
            "and view results."
        ),
        on_list_tools=on_list_tools,
        on_call_tool=on_call_tool,
    )


def _ok(data: Any) -> types.CallToolResult:
    text = json.dumps(data, separators=(",", ":"), ensure_ascii=False)
    return types.CallToolResult(
        content=[types.TextContent(type="text", text=text)],
    )


def _err(message: str) -> types.CallToolResult:
    return types.CallToolResult(
        content=[types.TextContent(type="text", text=message)],
        isError=True,
    )


def run(ctx: AppContext) -> None:
    logging.basicConfig(
        level=logging.WARNING,
        format="%(asctime)s [%(name)s] %(levelname)s: %(message)s",
    )
    _log.info("Starting ReactBench MCP server")
    server = _build_server(ctx)

    async def _main() -> None:
        async with stdio_server() as (read_stream, write_stream):
            await server.run(
                read_stream, write_stream, server.create_initialization_options()
            )

    anyio.run(_main)
