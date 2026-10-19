#!/usr/bin/env python3
"""close_cut.py —— 收口三件的通用腿（todo 5.8，cmd/PROMPT_055，2026-10-02）。
运行时契约：Python >= 3.13（3.12 兼容模式可用；解释器优先项目内 `.venv`，未建则系统，首次需要时建——5.32）＋ Git Bash（Windows）。详见 checks/check-env.sh。

用法：
  python dossier.py close-cut ROW CARD --commit|--defer --authorization REF --manifest FILE [--message TEXT] [--review FILE] [--queue N] [--dry-run]
  python dossier.py close-cut --status
  python dossier.py close-cut <行号> <卡号> --void "人原话" [--dry-run]   # 废除通道（5.17）：人裁作废的行搬入「## 废除」节；不与 --review/--queue 同用，只接人原话
  python dossier.py close-cut --selftest

普通收口先冻结本刀文件SHA256，提交并核对父提交、树和绑定内容后才释放锁。
--defer仅保存待提交状态；--status与cut-lock take共用同一核验。
恢复记录仅保留最近一次，住宿主.dossier/close-cut.json；它不是授权或业务验收。
不能凭工作区干净证明结案；不能强制阻止绕过入口或伪造授权。
"""
from __future__ import annotations

import argparse
import base64
import hashlib
import json
import os
import re
import subprocess
import sys
import tempfile
from datetime import date
from pathlib import Path

from ..paths import default_host
REPO = default_host()


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
    sess = REPO / "docs/SESSION.md"
    data = _read(sess)
    body = Path(review_file).read_bytes()  # 原样字节，不转码（卡面禁令）
    return [_write(sess, _review(data, body), dry)]


def _review(data: bytes, body: bytes) -> bytes:
    if _sep_shape(data)[1] == -1:
        raise ValueError("SESSION.md 找不到横线")
    if body.strip() in data:
        return data
    return data + (b"\n" if not data.endswith(b"\n") else b"") + body



def void_row(row: str, quote: str, dry: bool) -> list[str]:
    """废除通道（5.17）：人裁作废的行搬入 todo「## 废除」节，两行式；只接人原话。
    与 move_row 的差别：不勾、不写结案日期、不改已办——搬的是「不再做」，不是「做完了」。"""
    todo = REPO / "docs/TODO.md"
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
    todo = REPO / "docs/TODO.md"
    before = _read(todo)
    data = _move(before, row, card)
    if data == before:
        return [f"幂等：{row} 已结且已办有指针，无操作"]
    return [_write(todo, data, dry), f"MOVED {row} → 已办（两行式）"]


def _move(data: bytes, row: str, card: str) -> bytes:
    marker = f"- [x] **{row}**".encode()
    ptr = f"cmd/PROMPT_{card}.md".encode()
    if marker in data and ptr in data:
        return data
    open_marker = f"- [ ] **{row}**".encode()
    if open_marker not in data:
        raise ValueError(f"todo 里找不到未勾的 {row}")
    start = data.index(open_marker)
    m2 = re.search(rb"\r?\n\s*- \[ \] \*\*", data[start + 5 :])
    m3 = re.search(rb"\r?\n\r?\n", data[start + 5 :])
    best = min(
        [x for x in (m2.start() if m2 else None, m3.start() if m3 else None) if x is not None],
        default=None,
    )
    nl = 2 if best is not None and data[start + 5 + best : start + 7 + best] == b"\r\n" else 1
    cut = start + 5 + best + nl if best is not None else len(data)
    block = data[start:cut]
    if ptr not in block:
        raise ValueError("行块里没有本刀指针——先挂指针再收口")
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
    done = re.search(rb"- \[x\] \*\*", data)
    if done is None:
        section = re.search(rb"(?m)^## " + "已办".encode() + rb"[^\r\n]*(?:\r?\n|$)", data)
        if section is None:
            return data + (b"\n" if not data.endswith(b"\n") else b"") + "\n## 已办\n\n".encode() + entry
        return data[:section.end()] + b"\n" + entry + data[section.end():]
    anchor = done.start()
    data = data[:anchor] + entry + data[anchor:]
    return data


def advance_queue(qn: str, status: str, dry: bool) -> list[str]:
    q = REPO / "docs/queue.md"
    return [_write(q, _queue(q.read_bytes(), qn, status), dry), f"QUEUE #{qn} → {status}"]


def _queue(data: bytes, qn: str, status: str) -> bytes:
    s = data.decode("utf-8")
    pat = re.compile(rf"^(\| {int(qn)} \|[^|]+\|[^|]+\|) *[^|]+(\|.*)$", re.M)
    m = pat.search(s)
    if not m:
        raise ValueError(f"queue.md 没有 #{qn} 行——先在 queue.md 登记本刀再收口")
    s2 = pat.sub(lambda mm: f"{mm.group(1)} {status} {mm.group(2)}", s, count=1)
    # 下一未结行推进（「排队」或「在办」且非挂起/断点）
    nxt = re.compile(r"^(\| (\d+) \|[^|]+\|[^|]+\|) *(排队|在办) *(\|.*)$", re.M)
    m2 = next((m for m in nxt.finditer(s2) if int(m.group(2)) > int(qn)), None)
    if m2:
        s2 = s2[: m2.start()] + m2.group(1) + " 在办" + m2.group(4) + s2[m2.end() :]
    return s2.encode("utf-8")


def selftest() -> int:
    import shutil

    tmp = Path(tempfile.mkdtemp())
    fake = tmp / "repo"
    (fake / "docs").mkdir(parents=True)
    (fake / "docs/cmd").mkdir()
    global REPO
    real = REPO
    REPO = fake
    try:
        (fake / "docs/SESSION.md").write_bytes(
            "# s\n\n表\n\n---\n\n旧审阅\n".encode()
        )
        (fake / "docs/TODO.md").write_bytes(
            "# t\n\n- [ ] **9.9** 测试行 → `cmd/PROMPT_099.md`\n      细则行\n\n## 已办\n\n- [x] **8.8** 旧 → `cmd/PROMPT_088.md`\n".encode()
        )
        (fake / "docs/queue.md").write_text(
            "| 1 | a | C1 | 已结 | — |\n| 2 | b | 未写 | 排队 | — |\n", encoding="utf-8", newline=""
        )
        rv = tmp / "rev.md"
        rv.write_text("## 审查 · 新页\n\n结论：过\n", encoding="utf-8")
        ok = []
        # 1 搬行两行式
        ops = move_row("9.9", "099", dry=False)
        t = (fake / "docs/TODO.md").read_bytes()
        ok.append(("搬行两行式", b"- [x] **9.9**" in t and b"PROMPT_099.md" in t and t.count(b"- [ ] **9.9**") == 0))
        ok.append(("原措辞保留", "测试行".encode() in t))
        ok.append(("细则行随之移出", "细则行".encode() not in t))
        # 2 幂等
        ops2 = move_row("9.9", "099", dry=False)
        ok.append(("幂等", any("幂等" in o for o in ops2)))
        # 3 横线以下追加（LF 形 SESSION）
        ops3 = paste_review(str(rv), dry=False)
        s = (fake / "docs/SESSION.md").read_bytes()
        ok.append(("追加在横线以下", "## 审查 · 新页".encode() in s[si + 4 :] if (si := s.find(b"---")) != -1 else False))
        # 4 queue 推进
        ops4 = advance_queue("1", "已结", dry=False)
        q = (fake / "docs/queue.md").read_text(encoding="utf-8")
        ok.append(("queue 状态格", "| C1 | 已结 |" in q))
        # 5 干跑零写
        before = (fake / "docs/queue.md").read_bytes()
        advance_queue("2", "在办", dry=True)
        ok.append(("干跑零写", (fake / "docs/queue.md").read_bytes() == before))
        bad = [name for name, v in ok if not v]
        for name, v in ok:
            print(("PASS: " if v else "FAIL: ") + name)
        print("SELFTEST " + ("PASS" if not bad else "FAIL"))
        return 0 if not bad else 1
    finally:
        REPO = real
        shutil.rmtree(tmp, ignore_errors=True)


def _git(*args: str, check: bool = True) -> bytes:
    result = subprocess.run(["git", "-C", str(REPO), "--literal-pathspecs", *args],
                            capture_output=True, env={**os.environ, "GIT_OPTIONAL_LOCKS": "0"})
    if check and result.returncode:
        raise ValueError(f"git {args[0]}: {result.stderr.decode('utf-8', 'replace').strip()}")
    return result.stdout


def _head() -> tuple[str, str]:
    if any(os.environ.get(k) for k in ("GIT_DIR", "GIT_WORK_TREE", "GIT_INDEX_FILE", "GIT_COMMON_DIR")):
        raise ValueError("Git repository/index override is not supported")
    if Path(os.fsdecode(_git("rev-parse", "--show-toplevel")).strip()).resolve() != REPO.resolve():
        raise ValueError("host-root must be the Git work tree root")
    return (_git("rev-parse", "HEAD").decode().strip(),
            _git("symbolic-ref", "--quiet", "HEAD", check=False).decode().strip())


def _safe_path(name: str, *, inspect: bool = True) -> Path:
    # Explicit ordinary files only; no directory pathspecs, private state, links or Git links.
    if not isinstance(name, str) or not name or "\\" in name or ":" in name or any(ord(c) < 32 for c in name):
        raise ValueError(f"unsafe manifest path: {name!r}")
    parts = name.split("/")
    if any(x in ("", ".", "..") or x.endswith((".", " ")) for x in parts):
        raise ValueError(f"unsafe manifest path: {name}")
    if any(x.lower() in (".git", ".gitmodules", ".dossier", ".tmp", ".mail", ".ssh", ".aws")
           or x.lower().startswith(".env") or x.lower().endswith((".local.json", ".pem", ".key")) for x in parts):
        raise ValueError(f"private/temporary path: {name}")
    if not inspect:
        return REPO / name
    path = REPO
    for part in parts:
        path = path / part
        if path.is_symlink() or (hasattr(path, "is_junction") and path.is_junction()):
            raise ValueError(f"linked manifest path: {name}")
        if path != REPO / name and (path / ".git").exists():
            raise ValueError(f"nested repository: {name}")
    if path.exists() and not path.is_file():
        raise ValueError(f"not an ordinary file: {name}")
    indexed = _git("ls-files", "--stage", "--", name)
    historic = _git("ls-tree", "HEAD", "--", name)
    for listing in (indexed, historic):
        for entry in listing.splitlines():
            if entry and entry.split(None, 1)[0] not in (b"100644", b"100755"):
                raise ValueError(f"unsupported Git object: {name}")
    if _git("check-ignore", "--no-index", "--", name, check=False):
        raise ValueError(f"ignored/private manifest path: {name}")
    return path


def _digest(path: Path) -> str | None:
    return hashlib.sha256(path.read_bytes()).hexdigest() if path.exists() else None


def _manifest(data: object, *, inspect: bool = True) -> dict:
    if not isinstance(data, dict) or not data:
        raise ValueError("manifest must be a nonempty JSON path-to-SHA256 object")
    for name, digest in data.items():
        _safe_path(name, inspect=inspect)
        if digest is not None and (not isinstance(digest, str) or not re.fullmatch(r"[0-9a-f]{64}", digest)):
            raise ValueError(f"invalid SHA256: {name}")
    return data


def _valid_row(row: str) -> bool:
    return bool(row and row not in (".", "..") and not row.endswith((".", " "))
                and not any(c in "/\\:\x00" or ord(c) < 32 for c in row))


def _state_path() -> Path:
    path = REPO / ".dossier" / "close-cut.json"
    if path.is_symlink() or path.parent.is_symlink() or (hasattr(path.parent, "is_junction") and path.parent.is_junction()):
        raise ValueError("linked close-cut state is unsupported")
    return path


def _load() -> dict | None:
    path = _state_path()
    if not path.exists():
        return None
    r = json.loads(path.read_text(encoding="utf-8"))
    if (not isinstance(r, dict) or r.get("version") != 1 or r.get("phase") not in ("pending", "completed")
            or not isinstance(r.get("request"), dict) or not isinstance(r.get("before"), dict)
            or not isinstance(r.get("after"), dict) or not isinstance(r.get("base"), str)
            or not isinstance(r.get("branch"), str)):
        raise ValueError("damaged close-cut record")
    req = r["request"]
    if not all(isinstance(req.get(x), str) and req[x] for x in ("row", "card", "authorization")):
        raise ValueError("damaged close-cut request")
    if not _valid_row(req["row"]) or not req["card"].isdigit():
        raise ValueError("damaged row/card")
    _manifest(req.get("manifest"), inspect=False)
    if not re.fullmatch(r"[0-9a-f]{40}|[0-9a-f]{64}", r["base"]):
        raise ValueError("damaged base commit")
    for name, encoded in r["before"].items():
        _safe_path(name, inspect=False)
        base64.b64decode(encoded, validate=True)
    if set(r["before"]) != set(r["after"]):
        raise ValueError("damaged closure content")
    for encoded in r["after"].values():
        base64.b64decode(encoded, validate=True)
    if not set(r["before"]).issubset(req["manifest"]):
        raise ValueError("unbound closure content")
    if r.get("expected_tree") is not None:
        if (not isinstance(r.get("expected_tree"), str)
                or not re.fullmatch(r"[0-9a-f]{40}|[0-9a-f]{64}", r["expected_tree"])
                or not isinstance(r.get("bindings"), dict)
                or set(r["bindings"]) != set(req["manifest"])):
            raise ValueError("missing/damaged Git bindings")
    return r


def _save(record: dict) -> None:
    path = _state_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, name = tempfile.mkstemp(prefix=".close-cut-", dir=path.parent)
    try:
        with os.fdopen(fd, "w", encoding="utf-8", newline="\n") as f:
            json.dump(record, f, ensure_ascii=False, indent=2)
            f.write("\n")
            f.flush()
            os.fsync(f.fileno())
        os.replace(name, path)
    finally:
        if os.path.exists(name):
            os.unlink(name)


def _bound_commit(record: dict, commit: str) -> bool:
    tree = record.get("expected_tree")
    if not tree or not record.get("bindings"):
        return False
    actual = _git("show", "-s", "--format=%T%n%P", commit).decode().splitlines()
    if actual != [tree, record["base"]]:
        return False
    for name, wanted in record["bindings"].items():
        actual_entry = _git("ls-tree", commit, "--", name).decode("utf-8").strip()
        if actual_entry != wanted:
            return False
    return True


def closure_status(host: Path | None = None) -> tuple[int, str]:
    """The one read-only gate shared by status and cut-lock.take."""
    global REPO
    previous = REPO
    if host is not None:
        REPO = Path(host)
    try:
        record = _load()
        if record is None:
            return 0, "NO CLOSE-CUT RECORD (legacy host; no historical inference)"
        head, _ = _head()
        if record["phase"] != "completed":
            return 1, "PENDING: " + record.get("reason", "待提交/恢复")
        commit = record.get("commit")
        if (not isinstance(commit, str) or not re.fullmatch(r"[0-9a-f]{40}|[0-9a-f]{64}", commit)
                or not _bound_commit(record, commit)):
            return 1, "FAIL: completed record has no matching commit"
        test = subprocess.run(["git", "-C", str(REPO), "merge-base", "--is-ancestor", commit, head],
                              capture_output=True, env={**os.environ, "GIT_OPTIONAL_LOCKS": "0"})
        if test.returncode:
            return 1, "FAIL: recorded commit is outside the current history"
        return 0, f"COMPLETED {record['request']['row']} {commit}"
    except (OSError, ValueError, KeyError, TypeError) as exc:
        return 1, f"FAIL: close-cut state: {exc}"
    finally:
        REPO = previous


def _working(record: dict) -> None:
    for name, wanted in record["request"]["manifest"].items():
        current = _digest(_safe_path(name))
        allowed = {wanted}
        if name in record["after"]:
            for snapshot in (record["before"], record["after"]):
                allowed.add(hashlib.sha256(base64.b64decode(snapshot[name])).hexdigest())
        if current not in allowed:
            raise ValueError(f"frozen content drift: {name}")


def _index_safe(record: dict, *, all_paths: bool = False) -> None:
    manifest = record["request"]["manifest"]
    changed = _git("diff", "--cached", "--name-only", "--no-renames", "-z").split(b"\0")
    names = [raw.decode("utf-8") for raw in filter(None, changed)]
    for name in names:
        if name not in manifest:
            raise ValueError(f"unrelated staged content: {name}")
    for name in (manifest if all_paths else names):
        path = _safe_path(name)
        entry = _git("ls-files", "--stage", "--", name).decode("utf-8").strip()
        if not path.exists():
            if entry:
                raise ValueError(f"staged content differs from frozen deletion: {name}")
        else:
            oid = subprocess.run(
                ["git", "-C", str(REPO), "hash-object", "--path", name, "--stdin"],
                input=path.read_bytes(), capture_output=True, check=True).stdout
            if not entry or entry.split()[1] != oid.decode().strip() or entry.split()[2] != "0":
                raise ValueError(f"partial/unmerged staged content: {name}")


def _new_record(args, manifest: dict, review: bytes | None) -> dict:
    head, branch = _head()
    closure = {"docs/TODO.md", "docs/SESSION.md"}
    if args.queue:
        closure.add("docs/queue.md")
    if not closure.issubset(manifest) or any(manifest[x] is None for x in closure):
        raise ValueError("manifest must freeze TODO/SESSION and queue when used")
    for name, wanted in manifest.items():
        if _digest(_safe_path(name)) != wanted:
            raise ValueError(f"frozen content drift: {name}")
        if wanted is None and not _git("ls-tree", head, "--", name):
            raise ValueError(f"deletion has no tracked file: {name}")
    before = {name: base64.b64encode((REPO / name).read_bytes()).decode() for name in sorted(closure)}
    after = dict(before)
    after["docs/TODO.md"] = base64.b64encode(_move(base64.b64decode(before["docs/TODO.md"]), args.row, args.card)).decode()
    if after["docs/TODO.md"] == before["docs/TODO.md"]:
        raise ValueError("row is already marked closed without this commit record")
    if review is not None:
        after["docs/SESSION.md"] = base64.b64encode(_review(base64.b64decode(before["docs/SESSION.md"]), review)).decode()
    if args.queue:
        after["docs/queue.md"] = base64.b64encode(_queue(base64.b64decode(before["docs/queue.md"]), *args.queue)).decode()
    return {"version": 1, "phase": "pending", "reason": "待提交", "base": head, "branch": branch,
            "request": {"row": args.row, "card": args.card, "authorization": args.authorization,
                        "manifest": manifest, "review": hashlib.sha256(review).hexdigest() if review is not None else None,
                        "queue": args.queue, "message": args.message},
            "before": before, "after": after, "expected_tree": None, "bindings": {}}


def _finish(record: dict, commit: str) -> None:
    if not _bound_commit(record, commit):
        raise ValueError("actual commit parent/tree/content differs from expected closure")
    record.update(phase="completed", commit=commit, reason="Git commit verified")
    _save(record)
    lock = REPO / ".tmp" / "locks" / f"{record['request']['row']}.lock"
    if lock.exists():
        if lock.is_symlink():
            raise ValueError("linked lock is unsupported")
        lock.unlink()
    print(f"COMPLETED {record['request']['row']} {commit}")


def close(args) -> int:
    manifest = _manifest(json.loads(Path(args.manifest).read_text(encoding="utf-8")))
    review = Path(args.review).read_bytes() if args.review else None
    old = _load()
    same = old and old["request"]["row"] == args.row and old["request"]["card"] == args.card
    if same:
        record = old
        wanted = {"row": args.row, "card": args.card, "authorization": args.authorization,
                  "manifest": manifest, "review": hashlib.sha256(review).hexdigest() if review is not None else None,
                  "queue": args.queue, "message": args.message}
        # A deferred request may receive a later explicit commit authorization/message.
        original = dict(record["request"])
        if record["phase"] == "pending":
            original.update(authorization=args.authorization, message=args.message)
        if original != wanted:
            raise ValueError("recovery request differs from recorded frozen operation")
        if record["phase"] == "completed":
            code, text = closure_status()
            if code:
                raise ValueError(text)
            if not args.dry_run:
                _finish(record, record["commit"])
            else:
                print("DRY " + text)
            return 0
        record["request"] = wanted
    else:
        code, text = closure_status()
        if code:
            raise ValueError(text)
        record = _new_record(args, manifest, review)
    head, branch = _head()
    if branch != record["branch"]:
        raise ValueError("branch changed since close-cut began")
    if head != record["base"]:
        if args.commit and _bound_commit(record, head):
            if args.dry_run:
                print("DRY matching commit exists; would finish without another commit")
            else:
                _finish(record, head)
            return 0
        raise ValueError("HEAD changed; no matching closure commit at HEAD")
    _working(record)
    _index_safe(record)
    if args.dry_run:
        print("DRY frozen content/index verified; no files, objects, index or locks written")
        return 0
    record["reason"] = "explicit defer; 验收完成，待提交" if args.defer else "commit in progress; 待提交"
    _save(record)  # Durable pending state always precedes ledger/index mutation.
    if args.defer:
        print("PENDING: 验收完成，待提交 (TODO/queue/lock unchanged)")
        return 0
    try:
        for name, encoded in record["after"].items():
            (REPO / name).write_bytes(base64.b64decode(encoded))
        _working(record)
        _git("add", "--", *sorted(manifest))
        _index_safe(record, all_paths=True)
        tree = _git("write-tree").decode().strip()
        delta = _git("diff-tree", "--no-commit-id", "--name-only", "--no-renames", "-r", "-z", record["base"], tree)
        if any(raw.decode("utf-8") not in manifest for raw in filter(None, delta.split(b"\0"))):
            raise ValueError("expected tree contains unrelated staged changes")
        if record["expected_tree"] and tree != record["expected_tree"]:
            raise ValueError("index tree changed during recovery")
        record["expected_tree"] = tree
        record["bindings"] = {name: _git("ls-tree", tree, "--", name).decode("utf-8").strip() for name in manifest}
        _save(record)
        if _head() != (record["base"], record["branch"]):
            raise ValueError("HEAD/branch changed before commit")
        result = subprocess.run(["git", "-C", str(REPO), "commit", "-m", args.message], capture_output=True)
        print(result.stdout.decode("utf-8", "replace"), end="")
        if result.returncode:
            raise ValueError("git commit failed: " + result.stderr.decode("utf-8", "replace").strip())
        commit, actual_branch = _head()
        if actual_branch != record["branch"]:
            raise ValueError("branch changed during commit")
        _finish(record, commit)
        return 0
    except (OSError, ValueError, subprocess.CalledProcessError) as exc:
        record.update(phase="pending", reason=str(exc))
        _save(record)
        raise


def parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("row", nargs="?")
    p.add_argument("card", nargs="?")
    mode = p.add_mutually_exclusive_group()
    mode.add_argument("--commit", action="store_true")
    mode.add_argument("--defer", action="store_true")
    mode.add_argument("--void", metavar="QUOTE")
    p.add_argument("--authorization")
    p.add_argument("--manifest")
    p.add_argument("--message")
    p.add_argument("--review")
    p.add_argument("--queue", nargs="+", metavar="N")
    p.add_argument("--dry-run", action="store_true")
    p.add_argument("--status", action="store_true")
    p.add_argument("--selftest", action="store_true")
    return p


def main() -> None:
    p = parser()
    args = p.parse_args()
    try:
        if args.selftest:
            sys.exit(selftest())
        if args.status:
            if any((args.row, args.card, args.commit, args.defer, args.void, args.manifest, args.authorization,
                    args.review, args.queue, args.message)):
                p.error("--status is a separate read-only entry")
            code, text = closure_status()
            print(text)
            sys.exit(code)
        if not args.row or not args.card or not _valid_row(args.row):
            p.error("row and card are required (row must be a safe filename token)")
        args.card = args.card.removeprefix("PROMPT_")
        if not re.fullmatch(r"[0-9]+", args.card):
            p.error("card must be a numeric card number")
        if args.void is not None:
            if any((args.review, args.queue, args.manifest, args.authorization, args.message)):
                p.error("--void does not combine with closure arguments")
            ops = void_row(args.row, args.void, args.dry_run)
            for op in ops:
                print(op)
            if any(op.startswith("FAIL") for op in ops):
                sys.exit(1)
            lock = REPO / ".tmp" / "locks" / f"{args.row}.lock"
            if lock.exists() and not args.dry_run:
                lock.unlink()
            sys.exit(0)
        if not (args.commit or args.defer) or not args.authorization or not args.manifest:
            p.error("ordinary closure requires --commit|--defer, --authorization and --manifest")
        if args.commit and not args.message:
            p.error("--commit requires --message")
        if args.queue:
            if len(args.queue) > 2 or not args.queue[0].isdigit():
                p.error("--queue N [STATUS]")
            args.queue = [args.queue[0], args.queue[1] if len(args.queue) == 2 else "已结"]
            if args.queue[1] != "已结":
                p.error("ordinary closure queue status must be 已结")
        sys.exit(close(args))
    except (OSError, ValueError, KeyError, TypeError, subprocess.CalledProcessError) as exc:
        print(f"FAIL: {exc}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
