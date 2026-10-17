#!/usr/bin/env python3
"""section_stamp.py —— 转译源标记节（`^## …（→ harness）`）的 git 内容戳。

谁加的：2026-10-06，todo 5.19 / cmd/PROMPT_082.md（工牌 b1，subagent builder）。
取法三样（span／元数据排除／EOL）以该卡裁定 1 为正身，本件是执行件，注释只指不抄。
母本不存戳表：现值现算，存表即覆盖表复活。

用法：
  python dossier.py section-stamp             # 一行一节：文件名<TAB>节名<TAB>hash
  python dossier.py section-stamp --selftest  # 伪树三断言

输出序＝文件字典序 × 节现序；key＝文件 basename＋节名逐字。
哈希对 EOL 形态恒等（逐行剥 \\r 后 git hash-object --stdin）——autocrlf 的 clone
树算出同值，同 6.11 render-stamp 先例（examples/figures/make_frame.py 节尾）。
"""
from __future__ import annotations

import argparse
import re
import subprocess
import sys
import tempfile
from pathlib import Path

from ..paths import SOURCE_ROOT
REPO = SOURCE_ROOT
SRC = REPO / "rules"
FILES = sorted([
    "workflow.md",
    "directory.md",
    "roles.md",
    "verify.md",
    "claude-code.md",
    "cursor.md",
])
SUF = "（→ harness）"
META_COUNT = re.compile(r"^本节共 \d+ 条可转译项")  # 计数行（裁定 1：元数据排除）
META_EXEMPT = "按桌改写，不配戳"  # 豁免声明行（裁定 3：形状唯一，v1 零豁免）


def _blob(data: str) -> str:
    """git 眼中哈希；无 git 或失败：print 错误并 exit 1。"""
    try:
        p = subprocess.run(
            ["git", "hash-object", "--stdin"],
            input=data, capture_output=True, text=True, encoding="utf-8",
        )
    except OSError as exc:
        print(f"ERROR: 调不动 git（hash-object --stdin）：{exc}", file=sys.stderr)
        sys.exit(1)
    if p.returncode != 0:
        print(
            f"ERROR: git hash-object --stdin 退出 {p.returncode}：{p.stderr.strip()}",
            file=sys.stderr,
        )
        sys.exit(1)
    return p.stdout.strip()


def stamps_of(path: Path) -> list[tuple[str, str]]:
    """[(节名, 哈希), …] 按节现序。span 与排除按卡裁定 1 执行，不自选。"""
    lines = path.read_bytes().decode("utf-8").split("\n")

    def bare(s: str) -> str:  # 逐行剥尾部 \r（仅此，不做其他 normalize）
        return s[:-1] if s.endswith("\r") else s

    heads = [
        i for i, raw in enumerate(lines)
        if bare(raw).startswith("## ") and bare(raw).endswith(SUF)
        and len(bare(raw)) > len("## ") + len(SUF)
    ]
    out: list[tuple[str, str]] = []
    for i in heads:
        nxt = next(  # 边界＝下一 `^## ` 行（任意二级标题，不限标记），EOF 止
            (k for k in range(i + 1, len(lines)) if bare(lines[k]).startswith("## ")),
            len(lines),
        )
        name = bare(lines[i])[len("## "):-len(SUF)]  # 节名逐字：剥前缀与后缀，别的不动
        body = []
        for raw in lines[i:nxt]:
            ln = bare(raw)
            if META_COUNT.match(ln) or ln == META_EXEMPT:
                continue  # 元数据不进 span（裁定 1）——刷计数／配豁免不 bump 戳
            body.append(ln)
        out.append((name, _blob("\n".join(body) + "\n")))
    return out


def _selftest() -> int:
    """伪树三断言：标题计入／元数据排除／剥 \\r（CRLF↔LF 同哈希）。"""
    v0 = (
        f"## 甲节{SUF}\r\n"
        "正文一\r\n"
        "本节共 3 条可转译项（伪树计数行）\n"
        "按桌改写，不配戳\r\n"
        f"## 乙节{SUF}\n"
        "正文二\r\n"
        "本节共 2 条可转译项（伪树计数行）\r\n"
        "## 丙节（无标记）\n"  # span 边界认的是下一 `^## `，不限标记——非标记节收口
        "正文三\n"
    )

    def stamps(txt: str) -> list[tuple[str, str]]:
        with tempfile.TemporaryDirectory() as td:
            f = Path(td) / "fake.md"
            f.write_bytes(txt.encode("utf-8"))
            return stamps_of(f)

    base = stamps(v0)
    ok = True

    def chk(label: str, got, want) -> None:
        nonlocal ok
        hit = got == want
        ok = ok and hit
        print(f"   [{'ok' if hit else 'FAIL'}] {label}")

    chk("伪树枚举恰两节（非标记节不进单）", len(base), 2)
    # 1 标题计入：标题行在 span 内，改名即哈希变
    t1 = stamps(v0.replace(f"## 乙节{SUF}", f"## 乙节改{SUF}"))
    chk("标题计入：乙节改名，哈希变", t1[1][1] != base[1][1], True)
    # 2 元数据排除：计数行与豁免行都不进 span——删掉任一，哈希不变
    t2a = stamps(v0.replace("本节共 3 条可转译项（伪树计数行）\n", ""))
    chk("元数据排除：删计数行，甲节哈希不变", t2a[0][1], base[0][1])
    t2b = stamps(v0.replace("按桌改写，不配戳\r\n", ""))
    chk("元数据排除：删豁免行，甲节哈希不变", t2b[0][1], base[0][1])
    # 3 剥 \r：整树 CRLF ↔ LF，逐节哈希全同
    t3 = stamps(v0.replace("\r\n", "\n"))
    chk("剥 \\r：CRLF 与 LF 同哈希", t3, base)

    if ok:
        print("SELFTEST PASS")
        return 0
    print("SELFTEST FAIL")
    return 1


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(
        description="转译源标记节的 git 内容戳（取法正身：docs/cmd/PROMPT_082.md 裁定 1）",
    )
    ap.add_argument("--selftest", action="store_true",
                    help="伪树三断言（标题计入／元数据排除／剥 \\r）")
    args = ap.parse_args(argv)
    if args.selftest:
        return _selftest()
    for fn in FILES:
        p = SRC / fn
        if not p.is_file():
            print(f"ERROR: {p} 不在盘上", file=sys.stderr)
            return 1
        for name, h in stamps_of(p):
            print(f"{fn}\t{name}\t{h}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
