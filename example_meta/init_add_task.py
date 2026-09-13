#!/usr/bin/env python3
"""add_task 的本体：写出干净起点。盘上那份夹是生成物，不入库。不进 docs_meta/tests/run.sh。"""
from __future__ import annotations

import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent / "add_task"

TODO = """# 待办

一次只做未勾的一行。代理不准自己勾。勾完移进「已办」，不删。

- [ ] **1.1 接口**：`src/plus.py` 里要有 `add(a, b)` → `design/plus.md`
- [ ] **1.2 红测**：`tests/test_plus.py` 先写 `2+2=4`，核还没有，必须红 → `design/plus.md`
- [ ] **1.3 实现**：写下 `add`，测转绿 → `design/plus.md`
- [ ] **1.4 收口**：假人读领班汇报，dumb 档回「是」，结案

## 已办

（还没有。）
"""

SESSION = """# 本刀运行态

还没点行。等人（假人）发令。

| | |
|---|---|
| **许可面** | （无卡） |
| **点的行** | （无） |
| **状态** | 等点行 |
"""

PLUS = """# plus

**权威：思路。** 不当红绿。红绿只认卡片和 `tests/test_plus.py`。

`add(a, b)` 返回两个数的和。验收句就一句：`2 + 2 = 4`。
"""

README = """# add_task

冒烟用的微型桌。核是 `add(a, b)`。假人在隔壁 `../human_fake/`，由它点行、发令。

本夹只预置 `docs/` 树和四行待办。`src/` `tests/` 空着，等假人点了再写。

复原干净起点：`python ../init_add_task.py`
"""


def wipe_glob(folder: Path, pattern: str) -> None:
    if not folder.is_dir():
        return
    for p in folder.glob(pattern):
        if p.is_file():
            p.unlink()


def main() -> None:
    for rel in (
        "docs/cmd",
        "docs/design",
        "src",
        "tests",
        ".tmp",
    ):
        (ROOT / rel).mkdir(parents=True, exist_ok=True)

    wipe_glob(ROOT / "src", "*.py")
    wipe_glob(ROOT / "tests", "test_*.py")
    wipe_glob(ROOT / "docs" / "cmd", "PROMPT_*.md")
    tmp = ROOT / ".tmp"
    for p in tmp.iterdir():
        if p.name == "README.md":
            continue
        if p.is_file():
            p.unlink()
        elif p.is_dir():
            shutil.rmtree(p)

    (ROOT / "README.md").write_text(README, encoding="utf-8")
    (ROOT / "docs" / "todo.md").write_text(TODO, encoding="utf-8")
    (ROOT / "docs" / "SESSION.md").write_text(SESSION, encoding="utf-8")
    (ROOT / "docs" / "design" / "plus.md").write_text(PLUS, encoding="utf-8")
    (ROOT / "docs" / "cmd" / ".gitkeep").write_text("", encoding="utf-8")
    (ROOT / "src" / ".gitkeep").write_text("", encoding="utf-8")
    (ROOT / "tests" / ".gitkeep").write_text("", encoding="utf-8")
    (ROOT / ".tmp" / "README.md").write_text("草稿。零权威，不准自称通过。\n", encoding="utf-8")
    print(f"add_task 已复原：{ROOT}")


if __name__ == "__main__":
    main()
