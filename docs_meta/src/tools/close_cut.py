#!/usr/bin/env python3
"""close_cut.py —— 收口三件的通用腿（todo 5.8，cmd/PROMPT_055，2026-10-02）。
运行时契约：Python >= 3.13（3.12 兼容模式可用；解释器优先项目内 `.venv`，未建则系统，首次需要时建——5.32）＋ Git Bash（Windows）。详见 docs_meta/tests/check-env.sh。

用法：
  python docs_meta/src/tools/close_cut.py <行号> <卡号> [--review <审查页文件>] [--queue <#> [<状态>]] [--dry-run]
  python docs_meta/src/tools/close_cut.py <行号> <卡号> --void "人原话" [--dry-run]   # 废除通道（5.17）：人裁作废的行搬入「## 废除」节；不与 --review/--queue 同用，只接人原话
  python docs_meta/src/tools/close_cut.py --selftest

三件（对应 workflow.md 收口纪律里可机械化的部分）：
  1 --review  审查页原样字节追加到 SESSION.md 横线以下（自动适配 --- 的 CRLF/LF 形状）
  2 搬行      todo.md 里 `- [ ] **<行号>**` 起的块 → 已办区顶，两行式（原措辞＋指针/日期行），原字不动
  3 --queue   queue.md 指定 # 行状态格改给定值（默认「已结」），下一「排队/在办」未结行改「在办」

安全件：--dry-run 只打印不落盘；幂等（目标行已是 - [x] 或已办有其指针 → 「已结，无操作」退出 0）；FAIL 以非零退出。
明约：搬行进已办后是两行式（原措辞首行＋指针/日期行）——待办块内的其余细则行随之移出 todo（已办区「一条只许占两行」的既有规矩），细则的正身永远在 cmd/ 卡里。
它是工具不是检查本：不进 run.sh；判据仍住卡上。
"""
from __future__ import annotations

import re
import sys
import tempfile
from datetime import date
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]


def _read(p: Path) -> bytes:
    return p.read_bytes()


def _write(p: Path, data: bytes, dry: bool) -> str:
    if not dry:
        p.write_bytes(data)
    return f"{'DRY ' if dry else ''}WRITE {p} ({len(data)} bytes)"


def _sep_shape(data: bytes) -> tuple[int, int]:
    """返回 SESSION 里最后一条横线的 (起点, 终点)，兼容 CRLF/LF。"""
    i = max(data.rfind(b"---\r\n"), data.rfind(b"---\n"))
    if i == -1:
        return (-1, -1)
    j = i + 5 if data[i : i + 5] == b"---\r\n" else i + 4
    return (i, j)


def paste_review(review_file: str, dry: bool) -> list[str]:
    sess = REPO / "docs_meta/docs/SESSION.md"
    data = _read(sess)
    body = Path(review_file).read_bytes()  # 原样字节，不转码（卡面禁令）
    _, end = _sep_shape(data)
    if end == -1:
        return ["FAIL: SESSION.md 找不到横线"]
    if body.strip() in data:
        return ["幂等：审查页已在 SESSION，无操作"]
    tail = b"\r\n" if not data[:end].endswith(b"\n") else b""
    nl = b"\r\n" if body.endswith(b"\n") else body  # 正文自带结尾就不补
    return [_write(sess, data[:end] + tail + body, dry)]



def void_row(row: str, quote: str, dry: bool) -> list[str]:
    """废除通道（5.17）：人裁作废的行搬入 todo「## 废除」节，两行式；只接人原话。
    与 move_row 的差别：不勾、不写结案日期、不改已办——搬的是「不再做」，不是「做完了」。"""
    todo = REPO / "docs_meta/docs/todo.md"
    lines = todo.read_text(encoding="utf-8").splitlines()
    out, moved, note = [], [], None
    for idx, ln in enumerate(lines):
        if ln.startswith("- [ ]") and f"**{row}**" in ln:
            note = f"      **废除**（人裁，原话逐字：「{quote}」）"
            moved = [ln, note]
            continue
        out.append(ln)
    if not moved:
        return [f"FAIL: 没找到在办行 {row}"]
    # 插入 ## 废除 节：找到节头，插在节尾（下一个 ## 或文件末）
    res, inserted = [], False
    in_void = False
    for ln in out:
        if ln.startswith("## ") and "废除" in ln:
            in_void = True; res.append(ln); continue
        if in_void and ln.startswith("## "):
            res.extend(moved); res.append(""); inserted = True; in_void = False
        res.append(ln)
    if in_void and not inserted:
        res.extend(moved); inserted = True
    if not inserted:
        return ["FAIL: todo.md 没找到「## 废除」节——先立法后用（5.17）"]
    if not dry:
        todo.write_text("\n".join(res) + "\n", encoding="utf-8")
    return [f"{'DRY ' if dry else ''}MOVED {row} → 废除（两行式，原话随行）"]

def move_row(row: str, card: str, dry: bool) -> list[str]:
    todo = REPO / "docs_meta/docs/todo.md"
    data = _read(todo)
    marker = f"- [x] **{row}**".encode()
    ptr = f"cmd/PROMPT_{card}.md".encode()
    if marker in data and ptr in data:
        return [f"幂等：{row} 已结且已办有指针，无操作"]
    open_marker = f"- [ ] **{row}**".encode()
    if open_marker not in data:
        return [f"FAIL: todo 里找不到未勾的 {row}，也不是已结（既不在待办也不在已办？）"]
    start = data.index(open_marker)
    m = re.search(rb"\r?\n\s*- \[ \] \*\*|\r?\n\r?\n\s*- \[ \]", data[start + 5 :])
    m2 = re.search(rb"\r?\n\s*- \[ \] \*\*", data[start + 5 :])
    m3 = re.search(rb"\r?\n\r?\n", data[start + 5 :])
    best = min(
        [x for x in (m2.start() if m2 else None, m3.start() if m3 else None) if x is not None],
        default=None,
    )
    nl = 2 if data[start + 5 + best : start + 7 + best] == b"\r\n" else 1
    cut = start + 5 + best + nl if best is not None else len(data)
    block = data[start:cut]
    assert ptr in block, "行块里没有本刀指针——先挂指针再收口"
    data = data[:start] + data[cut:]
    first = block.split(b"- [ ] **" + row.encode() + b"** ", 1)[1].split(b"\r\n")[0].split(b"\n")[0]
    inline_ptr = f"cmd/PROMPT_{card}.md".encode() in first  # 施工期挂的行内指针已随行搬来
    if inline_ptr:
        entry = (
            f"- [x] **{row}** ".encode() + first + b"\n"
            + f"      （{date.today().isoformat()} 结案）\n".encode()
        )
    else:
        entry = (
            f"- [x] **{row}** ".encode() + first + b"\n"
            + f"      → `cmd/PROMPT_{card}.md`（{date.today().isoformat()} 结案）\n".encode()
        )
    anchor = re.search(rb"- \[x\] \*\*", data).start()
    data = data[:anchor] + entry + data[anchor:]
    return [_write(todo, data, dry), f"MOVED {row} → 已办（两行式）"]


def advance_queue(qn: str, status: str, dry: bool) -> list[str]:
    q = REPO / "docs_meta/docs/queue.md"
    s = q.read_bytes().decode("utf-8")  # 3.12 兼容：不用 read_text(newline=)
    pat = re.compile(rf"^(\| {int(qn)} \|[^|]+\|[^|]+\|) *[^|]+(\|.*)$", re.M)
    m = pat.search(s)
    if not m:
        return [f"FAIL: queue.md 没有 #{qn} 行——先在 queue.md 登记本刀再收口"]
    s2 = pat.sub(lambda mm: f"{mm.group(1)} {status} {mm.group(2)}", s, count=1)
    ops = [_write(q, s2.encode("utf-8"), dry), f"QUEUE #{qn} → {status}"]
    # 下一未结行推进（「排队」或「在办」且非挂起/断点）
    nxt = re.compile(r"^(\| (\d+) \|[^|]+\|[^|]+\|) *(排队|在办)(\|.*)$", re.M)
    m2 = nxt.search(s2)
    if m2 and int(m2.group(2)) > int(qn):
        s2 = s2[: m2.start()] + m2.group(1) + " 在办" + m2.group(4) + s2[m2.end() :]
        ops.append(f"QUEUE #{m2.group(2)} 排队/在办 → 在办")
        ops[0] = _write(q, s2.encode("utf-8"), dry)
    return ops


def selftest() -> int:
    import shutil

    tmp = Path(tempfile.mkdtemp())
    fake = tmp / "repo"
    (fake / "docs_meta/docs").mkdir(parents=True)
    (fake / "docs_meta/docs/cmd").mkdir()
    global REPO
    real = REPO
    REPO = fake
    try:
        (fake / "docs_meta/docs/SESSION.md").write_bytes(
            "# s\n\n表\n\n---\n\n旧审阅\n".encode()
        )
        (fake / "docs_meta/docs/todo.md").write_bytes(
            "# t\n\n- [ ] **9.9** 测试行 → `cmd/PROMPT_099.md`\n      细则行\n\n## 已办\n\n- [x] **8.8** 旧 → `cmd/PROMPT_088.md`\n".encode()
        )
        (fake / "docs_meta/docs/queue.md").write_text(
            "| 1 | a | C1 | 已结 | — |\n| 2 | b | 未写 | 排队 | — |\n", encoding="utf-8", newline=""
        )
        rv = tmp / "rev.md"
        rv.write_text("## 审查 · 新页\n\n结论：过\n", encoding="utf-8")
        ok = []
        # 1 搬行两行式
        ops = move_row("9.9", "099", dry=False)
        t = (fake / "docs_meta/docs/todo.md").read_bytes()
        ok.append(("搬行两行式", b"- [x] **9.9**" in t and b"PROMPT_099.md" in t and t.count(b"- [ ] **9.9**") == 0))
        ok.append(("原措辞保留", "测试行".encode() in t))
        ok.append(("细则行随之移出", "细则行".encode() not in t))
        # 2 幂等
        ops2 = move_row("9.9", "099", dry=False)
        ok.append(("幂等", any("幂等" in o for o in ops2)))
        # 3 横线以下追加（LF 形 SESSION）
        ops3 = paste_review(str(rv), dry=False)
        s = (fake / "docs_meta/docs/SESSION.md").read_bytes()
        ok.append(("追加在横线以下", "## 审查 · 新页".encode() in s[si + 4 :] if (si := s.find(b"---")) != -1 else False))
        # 4 queue 推进
        ops4 = advance_queue("1", "已结", dry=False)
        q = (fake / "docs_meta/docs/queue.md").read_text(encoding="utf-8")
        ok.append(("queue 状态格", "| C1 | 已结 |" in q))
        # 5 干跑零写
        before = (fake / "docs_meta/docs/queue.md").read_bytes()
        advance_queue("2", "在办", dry=True)
        ok.append(("干跑零写", (fake / "docs_meta/docs/queue.md").read_bytes() == before))
        bad = [name for name, v in ok if not v]
        for name, v in ok:
            print(("PASS: " if v else "FAIL: ") + name)
        print("SELFTEST " + ("PASS" if not bad else "FAIL"))
        return 0 if not bad else 1
    finally:
        REPO = real
        shutil.rmtree(tmp, ignore_errors=True)


def main() -> None:
    args = sys.argv[1:]
    if args[:1] == ["--selftest"]:
        sys.exit(selftest())
    if len(args) < 2:
        print(__doc__)
        sys.exit(2)
    row, card = args[0], args[1]
    card = card.removeprefix("PROMPT_")  # 全名短名都认（审查意见 3）
    review = None
    void_quote = None
    qn = None
    qstatus = "已结"
    dry = False
    i = 2
    while i < len(args):
        if args[i] == "--review":
            review = args[i + 1]; i += 2
        elif args[i] == "--queue":
            qn = args[i + 1]
            if i + 2 < len(args) and not args[i + 2].startswith("--"):
                qstatus = args[i + 2]; i += 3
            else:
                i += 2
        elif args[i] == "--void":
            void_quote = args[i + 1]; i += 2
        elif args[i] == "--dry-run":
            dry = True; i += 1
        else:
            print(f"不认的参数 {args[i]}"); sys.exit(2)
    ops: list[str] = []
    if void_quote is not None:
        if review is not None or qn is not None:
            print("FAIL: --void 不与 --review/--queue 同用"); sys.exit(1)
        ops += void_row(row, void_quote, dry)
    else:
        if review:
            ops += paste_review(review, dry)
        ops += move_row(row, card, dry)
        if qn:
            ops += advance_queue(qn, qstatus, dry)
    if qn:
        ops += advance_queue(qn, qstatus, dry)
    lock = REPO / ".tmp" / "locks" / f"{row}.lock"
    if lock.exists() and not any(o.startswith("FAIL") for o in ops):
        if not dry:
            lock.unlink()
        print(f"{'DRY ' if dry else ''}LOCK RELEASED {row}")
    for o in ops:
        print(o)
    if any(o.startswith("FAIL") for o in ops):
        sys.exit(1)


if __name__ == "__main__":
    main()
