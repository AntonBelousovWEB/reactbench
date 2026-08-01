"""python -m reactbench_mcp [command] [args...]

CLI mode:  python -m reactbench_mcp tasks --difficulty easy
MCP mode:  python -m reactbench_mcp
"""
import sys


def main() -> None:
    if len(sys.argv) < 2:
        from reactbench_mcp.app import wire
        from reactbench_mcp.server import run as run_server
        run_server(wire())
    else:
        from reactbench_mcp.cli.dispatch import run_cli
        run_cli(sys.argv[1], sys.argv[2:])


if __name__ == "__main__":
    main()
