#!/usr/bin/env bash

# todo 5.9 的运行时契约自检；出处：cmd/PROMPT_058.md。
# 本脚本按 UTF-8 输出；FAIL 只由 B/C 两段置位。
set -u

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd -P)"
fail_count=0

pass() { printf '[PASS] %s\n' "$1"; }
warn() { printf '[WARN] %s\n' "$1"; }
fail() { printf '[FAIL] %s\n' "$1"; fail_count=$((fail_count + 1)); }

# A：Python 3.13 是基准；3.12 已由 close_cut 兼容，所以只提示。
py_line="$(python -X utf8 -c 'import sys; print(f"Python {sys.version_info.major}.{sys.version_info.minor}"); sys.exit(0 if sys.version_info >= (3, 13) else 2)' 2>/dev/null)"
py_rc=$?
if (( py_rc == 0 )); then
    pass "A Python：$py_line（>= 3.13）"
elif (( py_rc == 2 )); then
    warn "A Python：$py_line（< 3.13；3.12 兼容模式可用）"
else
    warn "A Python：python 不可用或无法读取版本"
fi

# B：Windows 基准是 Git Bash（MSYS/Cygwin 形态）；WSL 直接判 FAIL。
bash_desc="$(uname -o 2>/dev/null)"
bash_rc=$?
bash_desc_lc="${bash_desc,,}"
if (( bash_rc != 0 )); then
    warn "B bash 形态：uname -o 不可读"
elif [[ "$bash_desc_lc" == *msys* || "$bash_desc_lc" == *cygwin* ]]; then
    pass "B bash 形态：$bash_desc（Git Bash）"
elif [[ "$bash_desc_lc" == *microsoft* || "$bash_desc_lc" == *linux* ]]; then
    fail "B bash 形态：$bash_desc（WSL）"
else
    warn "B bash 形态：$bash_desc（未识别；仅 WSL 判 FAIL）"
fi

# C：必须在 git work tree 内运行。
if git -C "$ROOT" rev-parse --is-inside-work-tree >/dev/null 2>&1; then
    pass "C git 仓库：git rev-parse --is-inside-work-tree 成功"
else
    fail "C git 仓库：git rev-parse --is-inside-work-tree 失败"
fi

# D：三处运行时声明必须在盘；缺任一只 WARN。
declare -a missing=()
if sed -n '1,40p' "$ROOT/docs_meta/src/tools/close_cut.py" | grep -q '^运行时契约：'; then :; else missing+=('close_cut.py 头部'); fi
if sed -n '1,40p' "$ROOT/docs_meta/src/init.py" | grep -q '^运行时契约：'; then :; else missing+=('init.py 头部'); fi
if grep -q 'check-env' "$ROOT/readme.md"; then :; else missing+=('readme.md'); fi
if (( ${#missing[@]} != 0 )); then
    warn "D 三处声明：缺 ${missing[*]}"
else
    pass "D 三处声明：close_cut.py、init.py、readme.md 均在盘"
fi

if (( fail_count != 0 )); then
    printf 'FAILED\n'
    exit 1
fi
printf 'ALL PASS\n'
