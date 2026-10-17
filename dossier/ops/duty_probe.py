#!/usr/bin/env python3
"""duty_probe.py —— 心跳 deadman 三面探针，只读谓词（todo 5.29，cmd/PROMPT_088）。

定位：值日手/巡查回路的定时件谓词载体——红即断点呈人，代理不自行修载体。

用法（无参）：
  python -X utf8 dossier.py duty-probe

三面判据：
  载体  schtasks /query /tn DossierQueueWake /fo LIST
        → Status（Ready/Running）、Last Result（0）、
          Scheduled Task State（Enabled）三项全过才绿；
  心跳  .tmp/queue-runner/wake.md 末条 `wake <ISO>` 距今 ≤15 分钟
        （任务周期 10 分钟，容睡醒赶点余量）；
  锁    .tmp/locks/*.lock 的 taken= 距今 >240 分钟即滞留红（阈同 cut_lock stale）。

查不到什么照写：
  monitor 耳现活查不到——耳死只能由消费缺口在 SESSION/git 活动侧暴露，
  不归本探针。本探针只读不写：不修、不建、不删任何盘件，只打印＋退出码；
  任一面红退出 1，否则 0。
"""
from __future__ import annotations

import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

from ..paths import SOURCE_ROOT, default_host
REPO = default_host()
WAKE = REPO / ".tmp" / "queue-runner" / "wake.md"
LOCKS = REPO / ".tmp" / "locks"

TASK = "DossierQueueWake"
WAKE_MAX_MIN = 15.0
LOCK_STALE_MIN = 240.0

WAKE_RE = re.compile(r"^wake\s+(\S+)")


def _age_minutes(stamp: str) -> float | None:
    """ISO 时戳距今分钟数；坏时戳返回 None（照写不修真相）。"""
    try:
        t = datetime.fromisoformat(stamp)
    except ValueError:
        return None
    if t.tzinfo is None:
        t = t.replace(tzinfo=timezone.utc)
    return (datetime.now(timezone.utc) - t).total_seconds() / 60


def probe_carrier() -> tuple[bool, str]:
    cmd = ["schtasks", "/query", "/tn", TASK, "/fo", "LIST", "/v"]
    try:
        r = subprocess.run(
            cmd, capture_output=True, timeout=30,
        )
    except (OSError, subprocess.SubprocessError) as e:
        return False, f"查询失败：{e}"
    text = r.stdout.decode("oem", errors="replace")
    fields: dict[str, str] = {}
    for line in text.splitlines():
        if ":" in line:
            key, _, val = line.partition(":")
            fields.setdefault(key.strip().lower(), val.strip())
    status = fields.get("status")
    last = fields.get("last result")
    state = fields.get("scheduled task state")
    if r.returncode != 0 or status is None or last is None or state is None:
        raw = (r.stderr.decode("oem", errors="replace").strip() or text.strip())
        return False, f"读不到三项（Status/Last Result/Scheduled Task State），原文：{raw[:200]}"
    ok = status in ("Ready", "Running") and last == "0" and "Enabled" in state
    detail = f"Status={status} / Last Result={last} / State={state}"
    return ok, detail


def probe_heartbeat() -> tuple[bool, str]:
    if not WAKE.exists():
        return False, f"心跳件缺失：{WAKE.relative_to(REPO).as_posix()}"
    stamp = None
    try:
        lines = WAKE.read_text(encoding="utf-8").splitlines()
    except OSError as e:
        return False, f"读心跳件失败：{e}"
    for line in lines:
        m = WAKE_RE.match(line.strip())
        if m:
            stamp = m.group(1)  # 末条 wake 为准
    if stamp is None:
        return False, "无 wake 条目"
    age = _age_minutes(stamp)
    if age is None:
        return False, f"坏时戳：{stamp}"
    return age <= WAKE_MAX_MIN, f"末条 wake {age:.1f} 分钟前（阈 {WAKE_MAX_MIN:.0f}）"


def probe_locks() -> tuple[bool, str]:
    stale: list[str] = []
    total = 0
    if LOCKS.exists():
        for p in sorted(LOCKS.glob("*.lock")):
            total += 1
            try:
                content = p.read_text(encoding="utf-8")
            except OSError:
                stale.append(f"{p.stem}(读失败)")
                continue
            taken = ""
            for line in content.splitlines():
                if line.startswith("taken="):
                    taken = line.removeprefix("taken=")
            age = _age_minutes(taken)
            if age is None:
                stale.append(f"{p.stem}(坏时戳)")
            elif age > LOCK_STALE_MIN:
                stale.append(f"{p.stem}({age:.0f} 分钟)")
    if stale:
        return False, "滞留锁：" + "、".join(stale)
    return True, f"{total} 把锁无滞留（阈 {LOCK_STALE_MIN:.0f} 分钟）"


def main() -> int:
    faces: list[tuple[str, bool, str]] = [
        ("载体", *probe_carrier()),
        ("心跳", *probe_heartbeat()),
        ("锁", *probe_locks()),
    ]
    for name, ok, detail in faces:
        print(f"{name}：{'绿' if ok else '红'}（{detail}）")
    reds = [name for name, ok, _ in faces if not ok]
    if reds:
        print(f"DEADMAN 总判：红（{'/'.join(reds)} 面红——断点呈人，代理不自行修载体）")
        return 1
    print("DEADMAN 总判：健康（载体/心跳/锁三面绿）")
    return 0


if __name__ == "__main__":
    sys.exit(main())
