# ReactBench MCP Server

MCP (Model Context Protocol) server for [ReactBench](https://reactbench.com) — evaluating coding agents on realistic React work. 52 tasks across 50+ open-source React repositories.

## Quickstart

```bash
cd reactbench/mcp-server
pip install -e .
python -m reactbench_mcp --check
python -m reactbench_mcp            # start MCP server
```

## MCP tools (7)

| Tool | When | Input | Output |
|------|------|-------|--------|
| `reactbench_list_tasks` | Once — discover | `difficulty?`, `category?`, `tags?`, `name_glob?` | Task IDs, diff, cat, tags |
| `reactbench_get_task` | Once — read instruction | `task_id` | Metadata, instruction, file tree |
| `reactbench_read_task_file` | Read specific file | `task_id`, `category`, `filename` | File contents |
| `reactbench_verify` | After writing ALL code | `task_id` | Instruction + hidden test specs |
| `reactbench_run_tasks` | Final grading only | `task_paths`, `agent`, `model`… | Harbor evaluation result |
| `reactbench_list_jobs` | After run_tasks | — | Job names, trial rewards |
| `reactbench_get_job_result` | Drill into job | `job_name` | Patches, diffstat, logs |

## Agent workflow

```
1. list_tasks  →  find task           (~50 tokens)
2. verify      →  instruction+tests   (~200–10K tokens)
3. [write ALL code]
4. vitest      →  verify locally      (free)
5. run_tasks   →  final Docker grade  (1× only)
```

## Token efficiency

See [`BENCHMARK.md`](./BENCHMARK.md) — 13 tasks, avg ~3 770 tokens.

## License

MIT — [Million Inc](https://million.dev)
