#!/usr/bin/env python3
"""postman.py —— 桌间邮局的两桌邮差（5.44，PROMPT_100）。

运行时契约：Python >= 3.13（3.12 兼容模式可用）＋ Git >= 2.37（`add --sparse`）。
远端收 `file://`、`https://`、`ssh://` 与 scp 形 `git@host:path` 四形。token 只从宿主私有件读：路径写在本桌
`.dossier/mail.json` 的 `token_file`，或放在环境变量 `DOSSIER_MAIL_TOKEN_FILE`；
变量里放的必须是路径，不是 token 值。token 值不进仓、不进聊天、不进日志。
"""
from __future__ import annotations

import argparse
import json
import os
import pathlib
import posixpath
import re
import subprocess
import sys
import tempfile
import urllib.parse
from datetime import datetime, timezone
from typing import Any


ADDRESS_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]*$")
SCP_REMOTE_RE = re.compile(r"^git@([A-Za-z0-9][A-Za-z0-9._-]*):(.+)$", re.DOTALL)
LETTER_TYPES = {
    "knife-report": "刀报要点：\n\n- 结果：\n- 判据：\n- 余项：\n",
    "breakpoint": "断点：\n\n- 现象：\n- 已做：\n- 下一步：\n",
    "help": "求助：\n\n- 需要：\n- 期限：\n",
    "request": "索件：\n\n- 所索：\n- 回投地址：\n",
    "notice": "通告：\n\n- 事项：\n- 生效时点：\n",
    "receipt": "回执：\n\n- 对来信：\n- 结论：\n",
}
HEADER_KEYS = ("from", "to", "date", "type", "subject")
CONFIG_NAME = ".dossier/mail.json"


class PostmanError(RuntimeError):
    """邮差拒绝继续；错误说明必须落 stderr。"""


def run_git(args: list[str], cwd: pathlib.Path, *, check: bool = True) -> subprocess.CompletedProcess[str]:
    env = os.environ.copy()
    env["GIT_TERMINAL_PROMPT"] = "0"
    env.setdefault("PYTHONUTF8", "1")
    proc = subprocess.run(
        ["git", *args],
        cwd=str(cwd),
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        env=env,
    )
    if check and proc.returncode != 0:
        detail = (proc.stderr.strip() or proc.stdout.strip() or "无附加读数")
        raise PostmanError(f"git {' '.join(args[:2])} 失败（退出码 {proc.returncode}）：{detail}")
    return proc


def normalize_url(url: str) -> tuple[str, str, str]:
    raw = url.strip()
    scp = SCP_REMOTE_RE.fullmatch(raw)
    if scp is not None:
        host = scp.group(1).lower()
        path = posixpath.normpath(urllib.parse.unquote(scp.group(2)))
        return ("ssh", host, path if path.startswith("/") else f"/{path}")

    parsed = urllib.parse.urlsplit(raw)
    if parsed.scheme not in {"file", "https", "ssh"}:
        raise PostmanError(
            f"邮局远端只收 file://、https://、ssh:// 与 git@host:path，当前是 {parsed.scheme or '无 scheme'}"
        )
    if parsed.scheme == "ssh":
        if parsed.password is not None or (parsed.username or "") not in {"", "git"}:
            raise PostmanError("SSH 邮局远端只收 git 用户且不许内嵌密码")
    elif parsed.username or parsed.password or "@" in (parsed.netloc or ""):
        raise PostmanError("邮局远端 URL 不许内嵌凭据")
    if parsed.scheme == "file":
        if parsed.netloc not in {"", "localhost"}:
            raise PostmanError("file:// 邮局远端不接受远程主机")
        path = posixpath.normpath(urllib.parse.unquote(parsed.path))
        return (parsed.scheme, "", path)
    host = parsed.hostname.lower() if parsed.hostname else ""
    if not host:
        raise PostmanError(f"{parsed.scheme}:// 邮局远端缺主机")
    port = parsed.port
    if parsed.scheme == "ssh" and port == 22:
        port = None
    netloc = host if port is None else f"{host}:{port}"
    path = posixpath.normpath(urllib.parse.unquote(parsed.path))
    return (parsed.scheme, netloc, path)


def same_url(left: str, right: str) -> bool:
    return normalize_url(left) == normalize_url(right)


def load_config(desk_root: pathlib.Path) -> dict[str, Any]:
    path = desk_root / CONFIG_NAME
    config: dict[str, Any] = {}
    if path.is_file():
        try:
            config = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            raise PostmanError(f"邮箱配置读不了（{path}）：{exc}") from exc
    config["desk"] = os.environ.get("DOSSIER_MAIL_DESK", config.get("desk", ""))
    config["post_office_url"] = os.environ.get(
        "DOSSIER_MAIL_URL", config.get("post_office_url", "")
    )
    token_file = os.environ.get("DOSSIER_MAIL_TOKEN_FILE", config.get("token_file", ""))
    if token_file:
        candidate = pathlib.Path(token_file).expanduser()
        if not candidate.is_absolute():
            candidate = (desk_root / candidate).resolve()
        config["token_file"] = str(candidate)
    else:
        config["token_file"] = ""
    return config


class Postman:
    def __init__(self, mail_path: pathlib.Path, *, load: bool = True):
        self.mail_path = mail_path.resolve()
        self.desk_root = self.mail_path.parent
        self.config = load_config(self.desk_root) if load else {}
        self.push_retries = 0

    @property
    def desk(self) -> str:
        return str(self.config.get("desk", ""))

    @property
    def own_dir(self) -> pathlib.Path:
        return self.mail_path / "desks" / self.desk

    @property
    def outbox(self) -> pathlib.Path:
        return self.own_dir / "outbox"

    @property
    def archive(self) -> pathlib.Path:
        return self.own_dir / "archive"

    @property
    def stranger(self) -> pathlib.Path:
        return self.own_dir / "stranger"

    def addresses(self) -> set[str]:
        book = self.mail_path / "address-book.md"
        if not book.is_file():
            raise PostmanError(f"地址簿不在：{book}")
        found: set[str] = set()
        for line in book.read_text(encoding="utf-8").splitlines():
            match = re.match(r"^-\s+([^\s]+)\s*$", line)
            if match:
                found.add(match.group(1))
        return found

    def remote_urls(self) -> list[str]:
        urls: list[str] = []
        fetch = run_git(["remote", "get-url", "origin"], cwd=self.mail_path, check=False)
        push = run_git(["remote", "get-url", "--push", "origin"], cwd=self.mail_path, check=False)
        if fetch.returncode != 0 or push.returncode != 0:
            raise PostmanError("邮局 submodule 缺 origin 远端")
        if fetch.stdout.strip():
            urls.append(fetch.stdout.strip())
        if push.stdout.strip():
            urls.append(push.stdout.strip())
        return list(dict.fromkeys(urls))

    def assert_post_office_remote(self) -> None:
        configured = str(self.config.get("post_office_url", ""))
        if not configured:
            raise PostmanError("邮局 URL 未配置；先由 init --with-mail 落 .dossier/mail.json")
        normalize_url(configured)
        urls = self.remote_urls()
        if not urls:
            raise PostmanError("origin 远端为空")
        bad = [url for url in urls if not same_url(configured, url)]
        if bad:
            raise PostmanError("push 三钉红：origin/pushURL 与邮局仓配置不一致，拒绝动远端")

    def run_push(self) -> subprocess.CompletedProcess[str]:
        configured = str(self.config.get("post_office_url", ""))
        if normalize_url(configured)[0] != "https":
            return run_git(["push", "origin", "main"], cwd=self.mail_path, check=False)
        token_file = pathlib.Path(str(self.config.get("token_file", "")))
        if not str(token_file):
            raise PostmanError("https 邮局缺 token 私件路径（DOSSIER_MAIL_TOKEN_FILE 只收路径）")
        if not token_file.is_file() or token_file.stat().st_size == 0:
            raise PostmanError("token 私件不在或为空；路径在，值不读进日志")
        with tempfile.TemporaryDirectory(prefix="dossier-postman-askpass-") as temporary:
            helper = pathlib.Path(temporary) / "askpass.sh"
            helper.write_text(
                "#!/bin/sh\ncase \"$1\" in\n"
                "  *Username*|*username*) printf '%s\\n' \"${DOSSIER_MAIL_USER:-x-access-token}\" ;;\n"
                "  *) cat \"$DOSSIER_MAIL_TOKEN_FILE\" ;;\n"
                "esac\n",
                encoding="ascii",
                newline="\n",
            )
            helper.chmod(0o700)
            env = os.environ.copy()
            env["GIT_TERMINAL_PROMPT"] = "0"
            env["GIT_ASKPASS"] = str(helper)
            env["DOSSIER_MAIL_TOKEN_FILE"] = str(token_file)
            return subprocess.run(
                ["git", "push", "origin", "main"],
                cwd=str(self.mail_path),
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
                env=env,
            )

    def pull_rebase(self) -> None:
        run_git(["pull", "--rebase", "origin", "main"], cwd=self.mail_path)

    def push_with_retry(self) -> None:
        self.assert_post_office_remote()
        attempts = max(1, int(self.config.get("push_attempts", 3)))
        # 这里的 token 临时件只包住一次 push；不落仓、不进输出。
        proc = self.run_push()
        if proc.returncode == 0:
            return
        for attempt in range(2, attempts + 1):
            self.push_retries += 1
            print(f"[RETRY] push 被拒（第 {attempt - 1} 次）；先 rebase 再重试", flush=True)
            self.pull_rebase()
            proc = self.run_push()
            if proc.returncode == 0:
                return
        detail = (proc.stderr.strip() or proc.stdout.strip() or "无附加读数")
        raise PostmanError(f"push 重试 {attempts} 次仍红：{detail}")

    def check(self) -> None:
        if not self.mail_path.is_dir():
            raise PostmanError(f".mail 不在：{self.mail_path}")
        top = run_git(["rev-parse", "--show-toplevel"], cwd=self.mail_path, check=False)
        if top.returncode != 0 or pathlib.Path(top.stdout.strip()).resolve() != self.mail_path:
            raise PostmanError(".mail 不是 Git 工作树")
        if not ADDRESS_RE.fullmatch(self.desk):
            raise PostmanError("desk 地址形不合法（只收字母数字点横线下划线）")
        self.assert_post_office_remote()
        branch = run_git(["branch", "--show-current"], cwd=self.mail_path)
        if branch.stdout.strip() != "main":
            raise PostmanError(f".mail 当前分支是 {branch.stdout.strip() or '空'}，只认 main")
        sparse = run_git(["sparse-checkout", "list"], cwd=self.mail_path, check=False)
        patterns = [line.strip() for line in sparse.stdout.splitlines() if line.strip()]
        if f"desks/{self.desk}" not in patterns:
            raise PostmanError(f"sparse 缺自己一格：desks/{self.desk}")
        if self.desk not in self.addresses():
            raise PostmanError(f"地址簿没有人签 {self.desk}")
        configured = str(self.config.get("post_office_url", ""))
        if normalize_url(configured)[0] == "https":
            token_file = pathlib.Path(str(self.config.get("token_file", "")))
            if not str(token_file):
                raise PostmanError("https 邮局缺 token 私件路径")
            if not token_file.is_file() or token_file.stat().st_size == 0:
                raise PostmanError("token 私件不在或为空")
        for needed in (self.outbox, self.archive, self.stranger):
            needed.mkdir(parents=True, exist_ok=True)
        print(f"[PASS] postman 自检：.mail、main、sparse、地址簿、远端三钉均就绪（desk={self.desk}）")

    def draft(self, to: str, letter_type: str, subject: str) -> pathlib.Path:
        if letter_type not in LETTER_TYPES:
            raise PostmanError(f"信型不在枚举：{letter_type}")
        if "\r" in subject or "\n" in subject:
            raise PostmanError("subject 不收换行")
        addresses = self.addresses()
        if self.desk not in addresses:
            raise PostmanError(f"发件地址未在人签地址簿：{self.desk}")
        if to not in addresses:
            raise PostmanError(f"收件地址未在人签地址簿：{to}")
        now = datetime.now(timezone.utc)
        stamp = now.strftime("%Y%m%dT%H%M%S") + f"{now.microsecond:06d}Z"
        path = self.outbox / f"draft-{stamp}.md"
        if path.exists():
            raise PostmanError(f"草稿名撞名：{path.name}")
        content = (
            f"from: {self.desk}\n"
            f"to: {to}\n"
            f"date: {now.isoformat(timespec='seconds')}\n"
            f"type: {letter_type}\n"
            f"subject: {subject}\n\n"
            f"{LETTER_TYPES[letter_type]}"
        )
        self.outbox.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8", newline="\n")
        print(f"[DRAFT] {path}")
        return path

    def resolve_draft(self, draft: str) -> pathlib.Path:
        candidate = pathlib.Path(draft).expanduser()
        if not candidate.is_absolute():
            candidate = self.outbox / candidate
        candidate = candidate.resolve()
        try:
            candidate.relative_to(self.outbox.resolve())
        except ValueError as exc:
            raise PostmanError("seal 只收自己 outbox 里的 draft") from exc
        if not candidate.is_file() or candidate.name.startswith("draft-") is False or candidate.suffix != ".md":
            raise PostmanError(f"不是可封草稿：{draft}")
        return candidate

    @staticmethod
    def parse_letter(path: pathlib.Path) -> dict[str, str]:
        lines = path.read_text(encoding="utf-8").splitlines()
        header: dict[str, str] = {}
        for line in lines:
            if not line.strip():
                break
            key, sep, value = line.partition(":")
            if sep and key.strip().lower() in HEADER_KEYS and key.strip().lower() not in header:
                header[key.strip().lower()] = value.strip()
        if tuple(header.keys()) != HEADER_KEYS:
            raise PostmanError(f"信头五字段不齐或顺序不对：{path.name}")
        return header

    def seal(self, draft: str) -> pathlib.Path:
        source = self.resolve_draft(draft)
        parsed = self.parse_letter(source)
        if parsed["from"] != self.desk:
            raise PostmanError("草稿发件人不是本桌")
        if parsed["to"] not in self.addresses():
            raise PostmanError("草稿收件人不在地址簿")
        if parsed["type"] not in LETTER_TYPES:
            raise PostmanError("草稿信型不在枚举")
        target = source.with_name(source.name.replace("draft-", "sealed-", 1))
        if target.exists():
            raise PostmanError(f"封缄名撞名：{target.name}")
        source.rename(target)
        print(f"[SEALED] {target}")
        return target

    def next_sequence(self) -> int:
        output = run_git(["ls-tree", "-r", "--name-only", "HEAD"], cwd=self.mail_path).stdout
        numbers = [0]
        for line in output.splitlines():
            match = re.search(r"/(?:inbox|archive)/([0-9]+)-[^/]+\.md$", line)
            if match:
                numbers.append(int(match.group(1)))
        return max(numbers) + 1

    def unique_path(self, directory: pathlib.Path, name: str) -> pathlib.Path:
        candidate = directory / name
        if not candidate.exists():
            return candidate
        stem = candidate.stem
        for index in range(1, 1000):
            candidate = directory / f"{stem}-{index}.md"
            if not candidate.exists():
                return candidate
        raise PostmanError(f"档名撞满：{name}")

    def send(self, *, skip_preflight: bool = False) -> list[pathlib.Path]:
        sealed = sorted(self.outbox.glob("sealed-*.md"))
        if not skip_preflight:
            self.pull_rebase()
        if not sealed:
            print("[READ] 无已封信，不投递")
            return []
        self.assert_post_office_remote()
        sequence = self.next_sequence()
        delivered: list[pathlib.Path] = []
        for letter in sealed:
            parsed = self.parse_letter(letter)
            if parsed["from"] != self.desk:
                raise PostmanError(f"已封信发件人不是本桌：{letter.name}")
            if parsed["to"] not in self.addresses():
                raise PostmanError(f"已封信收件人不在地址簿：{parsed['to']}")
            now = datetime.now(timezone.utc)
            stamp = now.strftime("%Y%m%dT%H%M%S") + f"{now.microsecond:06d}Z"
            name = f"{sequence:04d}-{parsed['from']}-{parsed['to']}-{stamp}.md"
            recipient = self.unique_path(self.mail_path / "desks" / parsed["to"] / "inbox", name)
            archive = self.unique_path(self.archive, name)
            content = letter.read_text(encoding="utf-8")
            recipient.parent.mkdir(parents=True, exist_ok=True)
            self.archive.mkdir(parents=True, exist_ok=True)
            recipient.write_text(content, encoding="utf-8", newline="\n")
            archive.write_text(content, encoding="utf-8", newline="\n")
            rel_recipient = recipient.relative_to(self.mail_path).as_posix()
            rel_archive = archive.relative_to(self.mail_path).as_posix()
            run_git(["add", "--sparse", "--", rel_recipient, rel_archive], cwd=self.mail_path)
            delivered.extend((recipient, archive))
            sequence += 1
            print(f"[POST] {rel_recipient}")
        run_git(
            ["commit", "-m", f"postman: post {len(sealed)} letters"],
            cwd=self.mail_path,
        )
        self.push_with_retry()
        for letter in sealed:
            letter.unlink()
        run_git(["sparse-checkout", "reapply"], cwd=self.mail_path)
        return delivered

    def receive(self) -> list[pathlib.Path]:
        self.pull_rebase()
        self.assert_post_office_remote()
        addresses = self.addresses()
        inbox = self.own_dir / "inbox"
        letters = sorted(inbox.glob("*.md"))
        if not letters:
            print("[READ] inbox 空")
            return []
        moved: list[pathlib.Path] = []
        stranger_count = 0
        for letter in letters:
            try:
                parsed = self.parse_letter(letter)
                known = parsed["from"] in addresses and parsed["to"] == self.desk
            except PostmanError:
                known = False
                parsed = {"from": "", "to": "", "subject": letter.name, **{"date": "", "type": ""}}
            destination_dir = self.archive if known else self.stranger
            destination_dir.mkdir(parents=True, exist_ok=True)
            destination = self.unique_path(destination_dir, letter.name)
            rel_source = letter.relative_to(self.mail_path).as_posix()
            rel_destination = destination.relative_to(self.mail_path).as_posix()
            run_git(["mv", "--", rel_source, rel_destination], cwd=self.mail_path)
            moved.append(destination)
            if known:
                print(f"[RECEIVED] {parsed['from']} → {self.desk}：{parsed['subject']}")
            else:
                stranger_count += 1
                print(f"[STRANGER] {rel_source} → 陌生件格")
        run_git(["commit", "-m", f"postman: receive {len(moved)} letters ({stranger_count} stranger)"], cwd=self.mail_path)
        self.push_with_retry()
        return moved


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="桌间邮差：draft → seal → send → receive")
    sub = parser.add_subparsers(dest="command", required=True)
    draft = sub.add_parser("draft", help="在人签地址簿内起草一封信")
    draft.add_argument("to")
    draft.add_argument("type", choices=sorted(LETTER_TYPES))
    draft.add_argument("subject")
    seal = sub.add_parser("seal", help="把 draft 改名 sealed；封缄才可投递")
    seal.add_argument("draft")
    sub.add_parser("send", help="把已封信投到收件 inbox，并留发件 archive")
    sub.add_parser("receive", help="清点 inbox；陌生件进陌生件格，已处理件进 archive")
    sub.add_parser("selftest", help="树外 bare 夹具两桌全周期自证")
    return parser.parse_args(argv)


def find_mail_path() -> pathlib.Path:
    override = os.environ.get("DOSSIER_MAIL_PATH")
    if override:
        return pathlib.Path(override).expanduser().resolve()
    cwd = pathlib.Path.cwd().resolve()
    if cwd.name == ".mail":
        return cwd
    return cwd / ".mail"

def attach_mail(desk_root: pathlib.Path, url: str, desk: str, *, dry_run: bool = False) -> Postman | None:
    """init 的可选适配器；不传旗时零影响。"""
    normalize_url(url)
    if not ADDRESS_RE.fullmatch(desk):
        raise PostmanError("desk 地址形不合法")
    inside = run_git(["rev-parse", "--is-inside-work-tree"], cwd=desk_root, check=False)
    if inside.returncode != 0 or inside.stdout.strip() != "true":
        raise PostmanError("init --with-mail 的靶子必须是 Git 工作树")
    mail_path = desk_root / ".mail"
    if dry_run:
        print(f"= 5.44 邮箱：dry-run 不挂 submodule（url 已验形，desk={desk}）")
        return None
    if not mail_path.exists():
        clone_args = [
            "clone", "--filter=blob:none", "--no-checkout", "--branch", "main",
            "--single-branch", url, ".mail",
        ]
        if normalize_url(url)[0] == "https":
            token_file = pathlib.Path(str(load_config(desk_root).get("token_file", "")))
            if str(token_file):
                if not token_file.is_file() or token_file.stat().st_size == 0:
                    raise PostmanError("token 私件不在或为空；路径在，值不读进日志")
                with tempfile.TemporaryDirectory(prefix="dossier-postman-askpass-") as temporary:
                    helper = pathlib.Path(temporary) / "askpass.sh"
                    helper.write_text(
                        "#!/bin/sh\ncase \"$1\" in\n"
                        "  *Username*|*username*) printf '%s\\n' \"${DOSSIER_MAIL_USER:-x-access-token}\" ;;\n"
                        "  *) cat \"$DOSSIER_MAIL_TOKEN_FILE\" ;;\n"
                        "esac\n",
                        encoding="ascii", newline="\n",
                    )
                    helper.chmod(0o700)
                    env = os.environ.copy()
                    env["GIT_TERMINAL_PROMPT"] = "0"
                    env["GIT_ASKPASS"] = str(helper)
                    env["DOSSIER_MAIL_TOKEN_FILE"] = str(token_file)
                    proc = subprocess.run(
                        ["git", *clone_args], cwd=str(desk_root), capture_output=True, text=True,
                        encoding="utf-8", errors="replace", env=env,
                    )
                    if proc.returncode != 0:
                        raise PostmanError(f"邮局 clone 失败（退出码 {proc.returncode}）")
            else:
                run_git(clone_args, cwd=desk_root)
        else:
            run_git(["-c", "protocol.file.allow=always", *clone_args], cwd=desk_root)
        head = run_git(["rev-parse", "HEAD"], cwd=mail_path).stdout.strip()
        run_git(["config", "--file", ".gitmodules", "submodule.mail.path", ".mail"], cwd=desk_root)
        run_git(["config", "--file", ".gitmodules", "submodule.mail.url", url], cwd=desk_root)
        run_git(["config", "--file", ".gitmodules", "submodule.mail.branch", "main"], cwd=desk_root)
        run_git(["config", "submodule.mail.path", ".mail"], cwd=desk_root)
        run_git(["config", "submodule.mail.url", url], cwd=desk_root)
        run_git(["config", "submodule.mail.branch", "main"], cwd=desk_root)
        run_git(["update-index", "--add", "--cacheinfo", f"160000,{head},.mail"], cwd=desk_root)
        run_git(["add", "--", ".gitmodules"], cwd=desk_root)
    elif not mail_path.is_dir():
        raise PostmanError(".mail 已存在但不是目录")
    else:
        registered = run_git(
            ["config", "--file", ".gitmodules", "--get", "submodule.mail.url"],
            cwd=desk_root, check=False,
        )
        if registered.returncode != 0 or not same_url(registered.stdout.strip(), url):
            raise PostmanError(".mail 已在但不是本卡要挂的邮局 submodule")
    run_git(["config", "core.autocrlf", "false"], cwd=mail_path)
    run_git(["sparse-checkout", "init", "--cone"], cwd=mail_path)
    run_git(["sparse-checkout", "set", "--cone", f"desks/{desk}"], cwd=mail_path)
    run_git(["checkout", "main"], cwd=mail_path)
    run_git(["config", "user.name", desk], cwd=mail_path)
    run_git(["config", "user.email", f"{desk}@postman.local"], cwd=mail_path)
    config_dir = desk_root / ".dossier"
    config_dir.mkdir(parents=True, exist_ok=True)
    config_path = config_dir / "mail.json"
    config: dict[str, Any] = {}
    if config_path.is_file():
        try:
            config = json.loads(config_path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            raise PostmanError(f"旧邮箱配置读不了：{exc}") from exc
    config.update({"version": 1, "desk": desk, "post_office_url": url, "push_attempts": 3})
    config_path.write_text(json.dumps(config, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
    postman = Postman(mail_path)
    postman.check()
    return postman


class Fixture:
    def __init__(self, root: pathlib.Path):
        self.root = root
        self.post_office = root / "post-office.git"
        self.uri = self.post_office.as_uri()

    def git(self, args: list[str], cwd: pathlib.Path) -> subprocess.CompletedProcess[str]:
        return run_git(args, cwd)

    def make_post_office(self) -> None:
        self.git(["init", "--bare", "-b", "main", str(self.post_office)], self.root)
        seed = self.root / "seed"
        self.git(["init", "-b", "main", str(seed)], self.root)
        for desk in ("demo-a", "demo-b", "demo-c"):
            for slot in ("inbox", "outbox", "archive"):
                directory = seed / "desks" / desk / slot
                directory.mkdir(parents=True, exist_ok=True)
                (directory / ".gitkeep").write_text("", encoding="utf-8")
        (seed / "address-book.md").write_text(
            "# address book\n- demo-a\n- demo-b\n- demo-c\n",
            encoding="utf-8",
            newline="\n",
        )
        self.git(["config", "user.email", "seed@postman.local"], seed)
        self.git(["config", "user.name", "seed"], seed)
        self.git(["config", "core.autocrlf", "false"], seed)
        self.git(["add", "-A"], seed)
        self.git(["commit", "-m", "seed"], seed)
        self.git(["remote", "add", "origin", self.uri], seed)
        self.git(["push", "-u", "origin", "main"], seed)

    def make_desk(self, name: str) -> pathlib.Path:
        desk_root = self.root / name
        mail = desk_root / ".mail"
        desk_root.mkdir(parents=True, exist_ok=True)
        self.git(["clone", "--filter=blob:none", "--no-checkout", "--branch", "main", self.uri, str(mail)], self.root)
        self.git(["config", "core.autocrlf", "false"], mail)
        self.git(["sparse-checkout", "init", "--cone"], mail)
        self.git(["sparse-checkout", "set", "--cone", f"desks/{name}"], mail)
        self.git(["checkout", "main"], mail)
        self.git(["config", "user.name", name], mail)
        self.git(["config", "user.email", f"{name}@postman.local"], mail)
        self.git(["config", "core.autocrlf", "false"], mail)
        config_dir = desk_root / ".dossier"
        config_dir.mkdir(parents=True, exist_ok=True)
        (config_dir / "mail.json").write_text(
            json.dumps(
                {"version": 1, "desk": name, "post_office_url": self.uri, "push_attempts": 3},
                ensure_ascii=False,
                indent=2,
            )
            + "\n",
            encoding="utf-8",
            newline="\n",
        )
        return desk_root

    def raw_post(self, mail: pathlib.Path, sender: str, recipient: str, sequence: int, subject: str) -> None:
        self.git(["pull", "--rebase", "origin", "main"], mail)
        now = datetime.now(timezone.utc).isoformat(timespec="seconds")
        name = f"{sequence:04d}-{sender}-{recipient}-{now.replace(':', '').replace('-', '').replace('+', 'Z')}.md"
        path = mail / "desks" / recipient / "inbox" / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(
            f"from: {sender}\nto: {recipient}\ndate: {now}\ntype: notice\nsubject: {subject}\n\nraw fixture\n",
            encoding="utf-8",
            newline="\n",
        )
        rel = path.relative_to(mail).as_posix()
        self.git(["add", "--sparse", "--", rel], mail)
        self.git(["commit", "-m", f"raw {sequence}"], mail)
        self.git(["push", "origin", "main"], mail)


def selftest() -> int:
    sys.stdout.reconfigure(encoding="utf-8")
    import tempfile

    with tempfile.TemporaryDirectory(prefix="dossier-postman-selftest-") as temporary:
        root = pathlib.Path(temporary).resolve()
        fixture = Fixture(root)
        print("== postman selftest ==")
        print(f"[READ] 夹具树（树外）：{root}")
        fixture.make_post_office()
        print("[PASS] bare 邮局：显式 main，seed 已推")
        a_root = fixture.make_desk("demo-a")
        b_root = fixture.make_desk("demo-b")
        a = Postman(a_root / ".mail")
        b = Postman(b_root / ".mail")
        if "blob:none" not in run_git(["config", "--get", "remote.origin.partialclonefilter"], a.mail_path).stdout:
            raise PostmanError("partial clone 未挂 blob:none")
        if (b.mail_path / "desks" / "demo-a").exists():
            raise PostmanError("sparse 泄出他桌目录")
        if not (a.mail_path / "address-book.md").is_file() or not (b.mail_path / "address-book.md").is_file():
            raise PostmanError("cone 根文件没露出地址簿")
        print("[PASS] 两桌夹具：partial clone＋sparse＋地址簿全员可见")
        first = a.draft("demo-b", "knife-report", "中文编码与首封信")
        first_sealed = a.seal(str(first))
        if not first_sealed.name.startswith("sealed-"):
            raise PostmanError("封缄未改名")
        a.send()
        if not (a.archive / first_sealed.name.replace("sealed-", "", 1)).exists():
            # 发件留底名以投递名为准；这里只要求档内有一枚新案卷。
            if not any(a.archive.glob("0001-demo-a-demo-b-*.md")):
                raise PostmanError("发件留底不在")
        b.receive()
        received = list((b.archive).glob("0001-demo-a-demo-b-*.md"))
        if len(received) != 1 or "中文编码与首封信" not in received[0].read_text(encoding="utf-8"):
            raise PostmanError("收件 archive 或中文读数不齐")
        print("[PASS] 全周期：draft→seal→send→receive→双方 archive；中文经 Python UTF-8 不花")
        second = a.draft("demo-b", "receipt", "防撞第二封")
        a.seal(str(second))
        a.send()
        if len(list(a.archive.glob("*-demo-a-demo-b-*.md"))) != 2:
            raise PostmanError("防撞读数不足两封")
        print("[PASS] 防撞：同一收发对第二封以唯一档名进 inbox/archive")
        c_root = fixture.make_desk("demo-c")
        c_mail = c_root / ".mail"
        third = a.draft("demo-b", "breakpoint", "落后基线重试")
        a.seal(str(third))
        fixture.raw_post(c_mail, "demo-c", "demo-b", 9000, "远端先行")
        a.send(skip_preflight=True)
        if a.push_retries < 1:
            raise PostmanError("重试剧本没有实际咬到被拒")
        print("[PASS] 重试：落后基线 push 被拒→rebase→重推成功")
        fixture.raw_post(c_mail, "demo-z", "demo-b", 9001, "陌生件")
        b.receive()
        strangers = list((b.mail_path / "desks" / "demo-b" / "stranger").glob("*.md"))
        if len(strangers) != 1:
            raise PostmanError("陌生件没有进陌生件格")
        print("[PASS] 陌生件：不在人签地址簿的来信只进陌生件格")
        https_left = "https://Example.invalid/mail.git"
        https_right = "https://example.invalid/mail.git"
        ssh_left = "ssh://git@Example.invalid:22/mail.git"
        ssh_right = "git@example.invalid:mail.git"
        accepted = (fixture.uri, https_left, ssh_left, ssh_right)
        for remote in accepted:
            normalize_url(remote)
        if not same_url(https_left, https_right) or not same_url(ssh_left, ssh_right):
            raise PostmanError("https 或 SSH 远端规范化坏")
        for bare in ("mail.git", "/tmp/mail.git", "D:/tmp/mail.git"):
            try:
                normalize_url(bare)
            except PostmanError:
                pass
            else:
                raise PostmanError(f"裸路径没有被拒绝：{bare}")
        print("[PASS] 远端四形：file/https/ssh/scp 收，裸路径拒；file:// 全周期已在上面实跑")
        print("postman selftest：ALL PASS")
    return 0


def main(argv: list[str] | None = None) -> int:
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
    args = parse_args(argv if argv is not None else sys.argv[1:])
    if args.command == "selftest":
        try:
            return selftest()
        except Exception as exc:
            print(f"postman selftest：FAILED——{exc}", file=sys.stderr)
            return 1
    postman = Postman(find_mail_path())
    try:
        if args.command == "draft":
            postman.draft(args.to, args.type, args.subject)
        elif args.command == "seal":
            postman.seal(args.draft)
        elif args.command == "send":
            postman.send()
        elif args.command == "receive":
            postman.receive()
        else:
            raise PostmanError(f"未知子命令：{args.command}")
    except Exception as exc:
        print(f"postman {args.command}：FAILED——{exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
