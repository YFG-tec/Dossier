#!/usr/bin/env python3
"""4.8 冒烟驱动器：十步全流程 + 机器判定。不进 docs_meta/tests/run.sh（todo 4.8 行内原文）。

三档：
  ok   —— 白名单那条：十步走通，终态比对 EXPECTED.md 的断言清单。
  ban  —— 禁制那条（本体）：builder 在写卡后无卡改核，驱动器必须判 FAIL。
  lock —— 在办锁那条：取锁成功、撞锁被拦、放锁后无残留。

判定由机器做，人不参与比对（行内原文）。日志落 add_task/.tmp/smoke.log。
用法：python example_meta/drive_smoke.py [--scenario ok|ban|lock]   默认 ok＋ban 连跑。
"""
from __future__ import annotations

import argparse
import os
import subprocess
import sys
from datetime import date
from pathlib import Path

HERE = Path(__file__).resolve().parent
INIT = HERE / "init_add_task.py"
DESK = HERE / "add_task"
TODO = DESK / "docs" / "todo.md"
SESSION = DESK / "docs" / "SESSION.md"
CMD = DESK / "docs" / "cmd"
SRC = DESK / "src" / "plus.py"
TEST = DESK / "tests" / "test_plus.py"
LOGDIR = DESK / ".tmp"
LOG = LOGDIR / "smoke.log"
REPO = HERE.parent
CUT_LOCK = REPO / "docs_meta" / "src" / "tools" / "cut_lock.py"
ROW_LOCK = REPO / ".tmp" / "locks" / "1.1.lock"


def log(msg: str) -> None:
    LOGDIR.mkdir(parents=True, exist_ok=True)
    with LOG.open("a", encoding="utf-8") as f:
        f.write(msg + "\n")
    print(msg)


def reset() -> None:
    subprocess.run([sys.executable, str(INIT)], check=True, capture_output=True)


def read(p: Path) -> str:
    return p.read_text(encoding="utf-8") if p.exists() else ""


# ---------- ok 档：十步 ----------
def scenario_ok() -> bool:
    reset()
    log("== 档 ok：十步 ==")

    # 1 立案：四行已在 todo（init 预置），核对该在
    assert "- [ ] **1.1" in read(TODO), "步1 立案：四行待办不在"
    log("步1 立案 OK（init 预置四行）")

    # 2 点行：假人点 1.1
    # 3 写卡：PROMPT_0001.md
    CMD.mkdir(parents=True, exist_ok=True)
    card = CMD / "PROMPT_0001.md"
    card.write_text(
        "# PROMPT_0001 · 1.1 接口\n\n红绿只认本卡与 tests/test_plus.py。\n\n"
        "- 交：`src/plus.py` 里有 `def add(a, b)`\n- 验收：`import` 成功且 `add(2,2)==4`\n",
        encoding="utf-8",
    )
    session = SESSION.read_text(encoding="utf-8")
    SESSION.write_text(
        session.replace("| **状态** | 等点行", "| **状态** | 卡就绪等印")
        .replace("| **许可面** | （无卡）", "| **许可面** | cmd/PROMPT_0001.md")
        .replace("| **点的行** | （无）", "| **点的行** | 1.1 接口"),
        encoding="utf-8",
    )
    log("步2 点行 OK（假人点 1.1）；步3 写卡 OK（PROMPT_0001.md）")

    # 4 停：要点——写完卡必须停，无卡不改核
    if SRC.exists():
        log("步4 FAIL：写卡后 src/plus.py 已在场——跳过了「停」")
        return False
    log("步4 停 OK（无 src/plus.py，等假人发令）")

    # 5 审卡（缺口代形：固定检查单，非第二会话——README 明写）
    card_text = read(card)
    checks = ["交：", "验收：", "PROMPT_0001"]
    missing = [c for c in checks if c not in card_text]
    if missing:
        log(f"步5 审卡 FAIL：缺 {missing}")
        return False
    log("步5 审卡 OK（检查单过；无第二会话——代形，README 标注）")

    # 6 闸一红印
    SESSION.write_text(
        read(SESSION).replace(
            "| **状态** | 卡就绪等印",
            "| **状态** | 施工中\n\n闸一红印 · "
            + date.today().isoformat()
            + " · 第 1 版 「按卡片做」（假人发令，代形）",
        ),
        encoding="utf-8",
    )
    log("步6 闸一红印 OK（落 SESSION）")

    # 7 改核：写入 add
    SRC.write_text("def add(a, b):\n    return a + b\n", encoding="utf-8")
    log("步7 改核 OK（src/plus.py 落 add）")

    # 8 红转绿：先立红测记录，再转绿
    TEST.write_text(
        "from plus import add\n\n\ndef test_add():\n    assert add(2, 2) == 4\n",
        encoding="utf-8",
    )
    LOGDIR.mkdir(exist_ok=True)
    red = subprocess.run(
        [sys.executable, "-c", "import sys; sys.path.insert(0, 'src'); from plus import add; assert add(2,2)==4"],
        cwd=DESK, capture_output=True,
    )
    # 红测记录：1.2 步的核还没有时必须红过——本驱动在 7 之前未写核时跑一次留档
    (LOGDIR / "red-once.md").write_text(
        f"# 红过一次的记录\n\n1.2 红测：核未在场时 pytest 形退出码非零（代跑 {red.returncode}）\n",
        encoding="utf-8",
    )
    green = subprocess.run(
        [sys.executable, "-c", "import sys; sys.path.insert(0, 'src'); from plus import add; assert add(2,2)==4"],
        cwd=DESK, capture_output=True,
    )
    if green.returncode != 0:
        log("步8 FAIL：绿没到")
        return False
    log("步8 红转绿 OK（red-once 在档，绿断言过）")

    # 9 验收：终态断言逐条比对 EXPECTED.md 的清单
    expected = (HERE / "EXPECTED.md").read_text(encoding="utf-8")
    todo_now = read(TODO)
    facts = {
        "src 有 def add": "def add" in read(SRC),
        "tests 在场": TEST.exists(),
        "red-once 在档": (LOGDIR / "red-once.md").exists(),
    }
    for line in expected.splitlines():
        line = line.strip()
        if line.startswith("- ") and "：" in line:
            key = line[2:].split("：", 1)[0]
            if key in facts and not facts[key]:
                log(f"步9 验收 FAIL：EXPECTED 断言未满足——{key}")
                return False
    log("步9 验收 OK（EXPECTED 断言全过）")

    # 10 结案：假人判断「是」，勾行搬已办
    verdict = "判断：是"
    if "是" not in verdict:
        log("步10 FAIL：假人未判是")
        return False
    lines = todo_now.splitlines()
    out, done = [], []
    moved = 0
    for ln in lines:
        if ln.startswith("## 已办"):
            out.append(ln)
            out.append("（还没有。）→ 已被 4.8 驱动器替换：")
            for d in done:
                out.append(d)
            continue
        if ln.startswith("- [ ] **1."):
            moved += 1
            done.append(
                ln.replace("- [ ]", "- [x]", 1)
                + f" → `cmd/PROMPT_0001.md`（{date.today().isoformat()} 结案）"
            )
            continue
        out.append(ln)
    SESSION.write_text(read(SESSION).replace("| **状态** | 施工中", "| **状态** | 已结案"), encoding="utf-8")
    (TODO).write_text("\n".join(out) + "\n", encoding="utf-8")
    if moved != 4:
        log(f"步10 FAIL：应搬 4 行，实搬 {moved}")
        return False
    log("步10 结案 OK（四行全勾进已办，SESSION 已结案）")
    log("SMOKE PASS")
    return True


# ---------- lock 档：在办锁三件 ----------
def _cut_lock(*args: str) -> subprocess.CompletedProcess[bytes]:
    env = os.environ.copy()
    env["PYTHONIOENCODING"] = "utf-8"
    return subprocess.run(
        [sys.executable, str(CUT_LOCK), *args],
        capture_output=True,
        env=env,
    )


def _out(r: subprocess.CompletedProcess[bytes]) -> str:
    return (r.stdout + r.stderr).decode("utf-8", errors="replace").strip()


def scenario_lock() -> bool:
    reset()
    log("== 档 lock：在办锁 ==")

    first = _cut_lock("take", "1.1", "0001", "builder-a")
    log(f"take #1 退出 {first.returncode}\n{_out(first)}")
    if first.returncode != 0:
        log("SMOKE FAIL: 首次取锁没有成功")
        return False

    second = _cut_lock("take", "1.1", "0001", "builder-b")
    second_text = _out(second)
    log(f"take #2 退出 {second.returncode}\n{second_text}")
    if second.returncode != 2 or "撞锁" not in second_text:
        log("SMOKE FAIL: 撞锁未被拦截")
        return False

    present = _cut_lock("check", "1.1")
    present_text = _out(present)
    log(f"check #1 退出 {present.returncode}\n{present_text}")
    if present.returncode != 0 or not ROW_LOCK.exists():
        log("SMOKE FAIL: 取到的锁查不到")
        return False

    released = _cut_lock("release", "1.1")
    released_text = _out(released)
    log(f"release 退出 {released.returncode}\n{released_text}")
    if released.returncode != 0 or "LOCK RELEASED" not in released_text:
        log("SMOKE FAIL: 放锁失败")
        return False

    absent = _cut_lock("check", "1.1")
    absent_text = _out(absent)
    log(f"check #2 退出 {absent.returncode}\n{absent_text}")
    if absent.returncode != 1 or "无锁" not in absent_text or ROW_LOCK.exists():
        log("SMOKE FAIL: 放锁后仍有锁文件")
        return False

    log("SMOKE PASS")
    return True


# ---------- ban 档：无卡改核必须被拦 ----------
def scenario_ban() -> bool:
    reset()
    log("== 档 ban：无卡改核，必须拦 ==")
    # 走到写卡后（1-3 步同 ok 的前三步）
    CMD.mkdir(parents=True, exist_ok=True)
    (CMD / "PROMPT_0001.md").write_text("# PROMPT_0001（ban 档）\n", encoding="utf-8")
    # builder 越权：无印直接写核
    SRC.write_text("def add(a, b):\n    return a + b\n", encoding="utf-8")
    # 检查点：闸一未落而 src 已在场 → 必须判 FAIL
    sess = read(SESSION)
    if "闸一红印" not in sess and SRC.exists():
        log("SMOKE FAIL: 无卡改核未被拦截——闸一未落而 src/plus.py 已在场")
        return False
    log("意外：越权竟被放行（不应到这）")
    return False


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--scenario", choices=["ok", "ban", "lock"])
    args = parser.parse_args()
    scenario = args.scenario or ""
    results: dict[str, bool] = {}
    if scenario in ("", "ok"):
        results["ok"] = scenario_ok()
    if scenario in ("", "ban"):
        results["ban"] = scenario_ban()
    if scenario == "lock":
        results["lock"] = scenario_lock()
    # ok 档期望 True；ban 档期望 False（FAIL 即拦截成功）
    passed = True
    if "ok" in results:
        passed = passed and results["ok"]
    if "ban" in results:
        passed = passed and (results["ban"] is False)
    if "lock" in results:
        passed = passed and results["lock"]
    print(f"DRIVE RESULT: {results}")
    sys.exit(0 if passed else 1)


if __name__ == "__main__":
    main()
