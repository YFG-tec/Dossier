# example_meta

冒烟夹。不进 `docs_meta/tests/run.sh`。等 `2.9`、`2.6` 都结案再跑全流程。

| | |
|---|---|
| `init_add_task.py` | `add_task/` 的本体。跑它才生成那张微型桌 |
| `add_task/` | 生成物，不入库。四行待办，核是 `add(a, b)` |
| `human_fake/` | 假人。dumb 只会「是」，reason 带一句理由 |

```text
python example_meta/init_add_task.py
```
