#!/usr/bin/env python3
"""假人 v0：读领班汇报，吐两行给领班。没配密钥则固定「是」。"""
from __future__ import annotations

import json
import os
import re
import sys
import urllib.error
import urllib.request
from pathlib import Path

HERE = Path(__file__).resolve().parent
ENV_PATH = HERE / ".env"
PROMPT_PATH = HERE / "prompt.md"
DEFAULT = "判断：是\n理由：\n"
MODES = ("dumb", "reason")


def load_env(path: Path) -> None:
    if not path.is_file():
        return
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, val = line.partition("=")
        key, val = key.strip(), val.strip().strip('"').strip("'")
        if key and key not in os.environ:
            os.environ[key] = val


def parse_args(argv: list[str]) -> tuple[str, str]:
    mode = ""
    path = ""
    rest = argv[1:]
    i = 0
    while i < len(rest):
        a = rest[i]
        if a == "--mode" and i + 1 < len(rest):
            mode = rest[i + 1].strip().lower()
            i += 2
            continue
        if a.startswith("--mode="):
            mode = a.split("=", 1)[1].strip().lower()
            i += 1
            continue
        if not path:
            path = a
            i += 1
            continue
        sys.stderr.write(f"用法: python human_fake.py [--mode dumb|reason] <领班汇报.md>\n")
        raise SystemExit(2)
    return mode, path


def resolve_mode(cli_mode: str) -> str:
    raw = cli_mode or os.environ.get("FAKE_HUMAN_MODE", "dumb")
    mode = raw.strip().lower()
    if mode not in MODES:
        sys.stderr.write(f"假人：未知模式 {raw!r}，可用 dumb / reason\n")
        raise SystemExit(2)
    return mode


def read_report(path: str) -> str:
    if path and path != "-":
        return Path(path).read_text(encoding="utf-8")
    if not path and sys.stdin.isatty():
        sys.stderr.write("用法: python human_fake.py [--mode dumb|reason] <领班汇报.md>\n")
        raise SystemExit(2)
    return sys.stdin.read()


def parse_reply(text: str) -> str:
    verdict = "是"
    reason = ""
    for line in text.replace("\r\n", "\n").splitlines():
        if line.startswith("判断："):
            raw = line[3:].strip()
            if raw in ("是", "否", "none"):
                verdict = raw
        elif line.startswith("理由："):
            reason = line[3:].strip()
    return f"判断：{verdict}\n理由：{reason}\n"


def _root(base: str) -> str:
    base = base.rstrip("/")
    for tail in ("/chat/completions", "/messages", "/v1"):
        if base.endswith(tail):
            base = base[: -len(tail)]
    return base.rstrip("/")


def _post(url: str, headers: dict, payload: dict) -> tuple[int, dict | None, str]:
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(url, data=data, method="POST", headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=90) as resp:
            raw = resp.read().decode("utf-8")
            return resp.status, json.loads(raw), ""
    except urllib.error.HTTPError as exc:
        raw = exc.read().decode("utf-8", "replace")
        try:
            return exc.code, json.loads(raw), raw[:160]
        except json.JSONDecodeError:
            return exc.code, None, raw[:160]
    except (urllib.error.URLError, TimeoutError, json.JSONDecodeError) as exc:
        return 0, None, str(exc)[:160]


def _content(payload: dict) -> str | None:
    if "choices" in payload:
        text = payload["choices"][0]["message"]["content"]
        return text if isinstance(text, str) else None
    blocks = payload.get("content")
    if isinstance(blocks, list) and blocks:
        text = blocks[0].get("text")
        return text if isinstance(text, str) else None
    return None


def ask_model(report: str) -> str:
    base = os.environ.get("FAKE_HUMAN_BASE_URL", "").rstrip("/")
    key = os.environ.get("FAKE_HUMAN_API_KEY", "").strip()
    model = os.environ.get("FAKE_HUMAN_MODEL", "").strip()
    if not (base and key and model):
        return DEFAULT

    system = PROMPT_PATH.read_text(encoding="utf-8")
    root = _root(base)
    attempts = [
        (
            f"{root}/v1/chat/completions",
            {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {key}",
            },
            {
                "model": model,
                "temperature": 0,
                "messages": [
                    {"role": "system", "content": system},
                    {"role": "user", "content": report},
                ],
            },
        ),
        (
            f"{root}/v1/messages",
            {
                "Content-Type": "application/json",
                "x-api-key": key,
                "anthropic-version": "2023-06-01",
            },
            {
                "model": model,
                "max_tokens": 256,
                "system": system,
                "messages": [{"role": "user", "content": report}],
            },
        ),
    ]

    last = ""
    for url, headers, payload in attempts:
        code, body, err = _post(url, headers, payload)
        if code == 200 and body:
            text = _content(body)
            if text and re.search(r"^判断：", text, re.M):
                sys.stderr.write(f"假人：通了 {url}\n")
                return parse_reply(text)
            last = f"{url} 回包对不上两行格式"
            continue
        last = f"{url} -> {code} {err}"

    sys.stderr.write(f"假人：模型没通，回落到 是（{last}）\n")
    return DEFAULT


def main() -> None:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", newline="\n")
    if hasattr(sys.stderr, "reconfigure"):
        sys.stderr.reconfigure(encoding="utf-8", newline="\n")
    load_env(ENV_PATH)
    cli_mode, path = parse_args(sys.argv)
    mode = resolve_mode(cli_mode)
    sys.stderr.write(f"假人：模式 {mode}\n")
    if mode == "dumb":
        sys.stdout.write(DEFAULT)
        return
    report = read_report(path)
    sys.stdout.write(ask_model(report))


if __name__ == "__main__":
    main()
