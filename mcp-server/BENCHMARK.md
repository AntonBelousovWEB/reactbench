# ReactBench MCP Server — Token Efficiency Benchmark

**Methodology**: each task queried via `reactbench_list_tasks` (to locate) + `reactbench_verify` (instruction + hidden tests). Optimal path = 2 MCP calls. Token estimate: `chars / 3.5`.

## Results (13 tasks, all categories)

| # | Task | Category | Difficulty | list_tasks | verify | Optimal (chars) | Tokens |
|---|------|----------|:----------:|:----------:|:------:|:---------------:|:------:|
| 1 | smoke | smoke | easy | 175 | 523 | 698 | ~200 |
| 2 | write-react (table) | real-repo | medium | 338 | 21 876 | 22 214 | ~6 350 |
| 3 | write-react (keyboard) | real-repo | medium | 305 | 21 136 | 21 441 | ~6 130 |
| 4 | write-react (tabs) | real-repo | hard | 323 | 7 332 | 7 655 | ~2 190 |
| 5 | fix-react (rd-health) | real-repo | hard | 292 | 520 | 812 | ~230 |
| 6 | write-react (jumper) | real-repo | hard | 339 | 1 418 | 1 757 | ~500 |
| 7 | fix-react (cloudscape) | real-repo | hard | 327 | 8 033 | 8 360 | ~2 390 |
| 8 | write-react (katex) | real-repo | hard | 302 | 10 347 | 10 649 | ~3 040 |
| 9 | write-react (accordion) | real-repo | hard | 292 | 12 370 | 12 662 | ~3 620 |
| 10 | fix-react (coreui) | real-repo | hard | 319 | 13 935 | 14 254 | ~4 070 |
| 11 | write-react (table resize) | real-repo | hard | 303 | 19 358 | 19 661 | ~5 620 |
| 12 | fix-react (vitest) | real-repo | hard | 273 | 17 230 | 17 503 | ~5 000 |
| 13 | write-react (gallery) | real-repo | hard | 341 | 33 630 | 33 971 | ~9 710 |

## Summary

| Metric | Value |
|--------|-------|
| Tasks tested | 13 |
| Categories | smoke, write-react, fix-react |
| Difficulty range | easy → hard |
| Avg tokens per task | **~3 770** |
| Median tokens | **~3 620** |
| Min tokens | ~200 (hello-react) |
| Max tokens | ~9 710 (gallery — large Playwright e2e) |

## Optimal agent pattern (2 MCP calls)

```
1. list_tasks (filtered)  →  find task        ~50–100 tokens
2. verify                 →  instruction+tests  ~200–10K tokens
3. [agent writes ALL code]
4. vitest/jest locally    →  verify            free
5. run_tasks              →  final Docker run  heavy, 1× only
```

Agents always spend **2 MCP calls** per task. Verification output size depends on test suite complexity, not task difficulty.
