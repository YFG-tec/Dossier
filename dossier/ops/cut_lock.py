#!/usr/bin/env python3
"""cut_lock.py —— 在办锁三件＋泄漏报告（todo 5.13，cmd/PROMPT_070）。

用法：
  python dossier.py cut-lock take <行号> <卡号> <agent>
  python dossier.py cut-lock check <行号>
  python dossier.py cut-lock release <行号>
  python dossier.py cut-lock stale [<分钟>]   # 默认 240
  python dossier.py cut-lock --selftest

锁文件固定在仓库根 `.tmp/locks/<行号>.lock`，三行：
  agent=<派单对象>
  taken=<ISO 时戳>
  cut=<卡号>

四规则：
  1 派单前查锁：撞锁即断点呈报。
  2 取锁即写：临时文件＋os.replace；撞锁永不覆盖。
  3 收口放锁：close_cut 末步自动；忘删由 stale 报警。
  4 锁零权威：丢了不废刀，只报警——git 才是事实。
"""
from __future__ import annotations

import argparse
import os
import shutil
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path

from ..paths import SOURCE_ROOT, default_host
REPO = default_host()
LOCKS = REPO / ".tmp" / "locks"


def _safe_row(row: str) -> None:
    if not row or "/" in row or "\\" in row or "\x00" in row or row in (".", ".."):
        raise ValueError(f"行号只能作文件名：{row!r}")


def _path(row: str) -> Path:
    _safe_row(row)
    return LOCKS / f"{row}.lock"


def _lines(p: Path) -> list[str]:
    try:
        return p.read_text(encoding="utf-8").splitlines()
    except OSError as e:
        return [f"读锁失败：{e}"]


def _three(lines: list[str]) -> list[str]:
    wanted = ("agent=", "taken=", "cut=")
    if len(lines) == 3 and all(x.startswith(y) for x, y in zip(lines, wanted)):
        return lines
    return lines  # 坏锁原样呈报，不在工具里修真相


def _atomic_take(row: str, card: str, agent: str) -> tuple[int, list[str]]:
    p = _path(row)
    LOCKS.mkdir(parents=True, exist_ok=True)
    data = (
        f"agent={agent}\n"
        f"taken={datetime.now(timezone.utc).isoformat(timespec='seconds')}\n"
        f"cut={card}\n"
    ).encode("utf-8")
    fd, name = tempfile.mkstemp(prefix=f".{row}.", suffix=".tmp", dir=LOCKS)
    temp = Path(name)
    try:
        with os.fdopen(fd, "wb") as f:
            f.write(data)
            f.flush()
            os.fsync(f.fileno())
        # os.link 先原子占位，保证并发时第二个 take 只会撞锁；
        # 随后 os.replace 仍是卡面要求的临时文件→锁文件原子落位。
        try:
            os.link(temp, p)
        except FileExistsError:
            return 2, ["撞锁：" + _collision(row)] + _three(_lines(p))
        os.replace(temp, p)
        return 0, data.decode("utf-8").splitlines()
    finally:
        try:
            temp.unlink()
        except FileNotFoundError:
            pass


def _collision(row: str) -> str:
    return f"{row} 已有锁"


def take(row: str, card: str, agent: str) -> int:
    try:
        p = _path(row)
    except ValueError as e:
        print(str(e))
        return 2
    if p.exists():
        print("撞锁：" + _collision(row))
        for line in _three(_lines(p)):
            print(line)
        return 2
    try:
        code, lines = _atomic_take(row, card, agent)
    except OSError as e:
        print(f"取锁失败：{e}")
        return 2
    for line in lines:
        print(line)
    return code


def check(row: str) -> int:
    try:
        p = _path(row)
        lines = _three(_lines(p))
    except ValueError as e:
        print(str(e))
        return 2
    if not p.exists():
        print("无锁")
        return 1
    for line in lines:
        print(line)
    return 0


def release(row: str) -> int:
    try:
        p = _path(row)
        p.unlink()
    except FileNotFoundError:
        print(f"ALREADY FREE {row}")
        return 0
    except ValueError as e:
        print(str(e))
        return 2
    print(f"LOCK RELEASED {row}")
    return 0


def _age_minutes(taken: str) -> float | None:
    try:
        stamp = taken.removeprefix("taken=")
        if stamp.endswith("Z"):
            stamp = stamp[:-1] + "+00:00"
        t = datetime.fromisoformat(stamp)
        if t.tzinfo is None:
            t = t.replace(tzinfo=timezone.utc)
        return (datetime.now(timezone.utc) - t).total_seconds() / 60
    except ValueError:
        return None


def stale(minutes: int = 240) -> int:
    found = False
    if LOCKS.exists():
        for p in sorted(LOCKS.glob("*.lock")):
            lines = _three(_lines(p))
            kv = {x.split("=", 1)[0]: x.split("=", 1)[1] for x in lines if "=" in x}
            age = _age_minutes(kv.get("taken", ""))
            if age is None or age > minutes:
                found = True
                shown = f"{age:.1f}" if age is not None else "坏时戳"
                print(f"STALE {p.stem} {shown} 分钟")
                for line in lines:
                    print(line)
    if not found:
        print("NO STALE LOCKS")
    return 1 if found else 0


def selftest() -> int:
    global LOCKS
    real = LOCKS
    root = Path(tempfile.mkdtemp())
    LOCKS = root / ".tmp" / "locks"
    try:
        ok: list[tuple[str, bool]] = []
        code = take("1.1", "070", "selftest")
        p = LOCKS / "1.1.lock"
        lines = _lines(p)
        ok.append(("原子取锁", code == 0 and p.exists() and len(lines) == 3 and lines[0].startswith("agent=") and lines[1].startswith("taken=") and lines[2] == "cut=070" and not list(LOCKS.glob("*.tmp"))))
        code2 = take("1.1", "070-2", "second")
        after = _lines(p)
        ok.append(("撞锁退出2且不覆盖", code2 == 2 and after == lines and after[2] == "cut=070"))
        ok.append(("check", check("1.1") == 0))
        ok.append(("release 幂等", release("1.1") == 0 and not p.exists() and release("1.1") == 0))
        take("2.2", "070", "selftest")
        ok.append(("stale 报告", stale(0) == 1 and (LOCKS / "2.2.lock").exists()))
        release("2.2")
        bad = [name for name, value in ok if not value]
        for name, value in ok:
            print(("PASS: " if value else "FAIL: ") + name)
        print("SELFTEST " + ("PASS" if not bad else "FAIL"))
        return 0 if not bad else 1
    finally:
        LOCKS = real
        shutil.rmtree(root, ignore_errors=True)


def parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--selftest", action="store_true", help="合成 tmp 夹具自检")
    sub = p.add_subparsers(dest="command", required=False)
    t = sub.add_parser("take", help="取锁；撞锁退出 2，永不覆盖")
    t.add_argument("row")
    t.add_argument("card")
    t.add_argument("agent")
    c = sub.add_parser("check", help="查锁；在退出 0，不在退出 1")
    c.add_argument("row")
    r = sub.add_parser("release", help="放锁；幂等，总退出 0")
    r.add_argument("row")
    s = sub.add_parser("stale", help="列锁龄超阈值的锁；有则退出 1")
    s.add_argument("minutes", nargs="?", type=int, default=240)
    return p


def main() -> None:
    p = parser()
    args = p.parse_args()
    if args.selftest:
        sys.exit(selftest())
    if args.command == "take":
        sys.exit(take(args.row, args.card, args.agent))
    if args.command == "check":
        sys.exit(check(args.row))
    if args.command == "release":
        sys.exit(release(args.row))
    if args.command == "stale":
        if args.minutes < 0:
            print("分钟阈值不能为负")
            sys.exit(2)
        sys.exit(stale(args.minutes))
    p.print_help()
    sys.exit(2)


if __name__ == "__main__":
    main()
