# example_meta

冒烟夹。不进 `docs_meta/tests/run.sh`。入口一条命令：

```text
python example_meta/drive_smoke.py               # 两档连跑（ok + ban）
python example_meta/drive_smoke.py --scenario ok  # 白名单那条：十步走通
python example_meta/drive_smoke.py --scenario ban # 禁制那条：无卡改核必须被拦（本体）
```

终态断言清单在 `EXPECTED.md`；**判定由机器做，人不参与比对**。每趟从干净起点开始（首步调 `init_add_task.py`），跑完可用同一条复原。

| | |
|---|---|
| `init_add_task.py` | `add_task/` 的本体。跑它才生成那张微型桌 |
| `add_task/` | 生成物，不入库。四行待办，核是 `add(a, b)` |
| `human_fake/` | 假人。dumb 只会「是」，reason 带一句理由 |
| `drive_smoke.py` | 十步驱动器，两档，退出码 0/1 |
| `EXPECTED.md` | ok 档终态断言清单 |

**两处已知缺口（与真流程的差异，明写不藏）**：①审卡那步没有第二会话，驱动器内以「读卡＋固定检查单」代形；②假人 v1 只会通过（dumb 硬编码），它是驱动器不是责任人——收紧归 contract-tester。低阶模型假人另立一行（todo），不在本夹。
