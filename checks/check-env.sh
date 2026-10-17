#!/usr/bin/env bash
source "$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd -P)/lib/paths.sh"

# During apply, this packaged probe runs from the already selected P before active
# is recorded. Verify its commit/tree; ordinary host checks require active A.
DOSSIER_EXECUTION_ROOT="$(python -B -X utf8 -c '
import sys
from pathlib import Path
sys.path.insert(0,sys.argv[1])
from dossier.paths import execution_source
from dossier.runtime import load, git, DEPENDENCY, status
source=Path(sys.argv[1]).resolve(); host=Path(sys.argv[2]).resolve(); state=load(host)
if state and state.get("phase")=="applying" and source==host/DEPENDENCY:
    if git(source,"rev-parse","HEAD").decode().strip()!=state["product_commit"]: raise RuntimeError("applying commit mismatch")
    if git(source,"rev-parse","HEAD^{tree}").decode().strip()!=state["target_tree"]: raise RuntimeError("applying tree mismatch")
    print(source)
else:
    if not status(host)["registered"]: print("Not decoupled; legacy source checks apply",file=sys.stderr)
    print(execution_source(host))
' "$DOSSIER_SOURCE_ROOT" "$ROOT")" || exit 1


# todo 5.9 的运行时契约自检；出处：cmd/PROMPT_058.md。
# 本脚本按 UTF-8 输出；FAIL 由 B/C/E 三段置位。
set -u

fail_count=0

pass() { printf '[PASS] %s\n' "$1"; }
warn() { printf '[WARN] %s\n' "$1"; }
fail() { printf '[FAIL] %s\n' "$1"; fail_count=$((fail_count + 1)); }

# A：Python 3.13 是基准；3.12 已由 close_cut 兼容，所以只提示。正身＝cmd/PROMPT_090.md 裁定 1（人裁①：惰性 venv，未建不算红）。
if [[ -x "$ROOT/.venv/Scripts/python.exe" ]]; then
    py_bin="$ROOT/.venv/Scripts/python.exe"
    py_tag="[venv]"
elif [[ -x "$ROOT/.venv/bin/python" ]]; then
    py_bin="$ROOT/.venv/bin/python"
    py_tag="[venv]"
else
    py_bin="python"
    py_tag="[系统·venv 未建——首次需要时建 5.32]"
fi
py_line="$($py_bin -X utf8 -c 'import sys; print(f"Python {sys.version_info.major}.{sys.version_info.minor}"); sys.exit(0 if sys.version_info >= (3, 13) else 2)' 2>/dev/null)"
py_rc=$?
if (( py_rc == 0 )); then
    pass "A Python$py_tag：$py_line（>= 3.13）"
elif (( py_rc == 2 )); then
    warn "A Python$py_tag：$py_line（< 3.13；3.12 兼容模式可用）"
else
    warn "A Python$py_tag：python 不可用或无法读取版本"
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
if sed -n '1,40p' "$DOSSIER_EXECUTION_ROOT/dossier/ops/close_cut.py" | grep -q '^运行时契约：'; then :; else missing+=('close_cut.py 头部'); fi
if sed -n '1,40p' "$DOSSIER_EXECUTION_ROOT/dossier/install.py" | grep -q '^运行时契约：'; then :; else missing+=('init.py 头部'); fi
if grep -q 'check-env' "$DOSSIER_EXECUTION_ROOT/readme.md"; then :; else missing+=('readme.md'); fi
if (( ${#missing[@]} != 0 )); then
    warn "D 三处声明：缺 ${missing[*]}"
else
    pass "D 三处声明：close_cut.py、init.py、readme.md 均在盘"
fi

# E：架构执行在场性（量程跟档位——5.20，PROMPT_083）。正身＝cmd/PROMPT_083.md 裁定 1。
# 只查在场配对，不查生效性——无实件可查的东西不写死（生效性深检待 hooks 等实件出现）。
e_agents_on=0
e_skills_on=0
e_sw_on=0
declare -a e_missing=()
if [[ -d "$ROOT/.claude/agents" ]]; then
    e_agents_on=1
    for f in builder contract-tester review spec-guard; do
        [[ -f "$ROOT/.claude/agents/$f.md" ]] || e_missing+=("agents/$f.md")
    done
fi
if [[ -d "$ROOT/.claude/skills" ]]; then
    e_skills_on=1
    for d in write-cmd one-slice example-report; do
        [[ -f "$ROOT/.claude/skills/$d/SKILL.md" ]] || e_missing+=("skills/$d/SKILL.md")
    done
fi
if [[ -d "$ROOT/.cursor" ]]; then
    e_sw_on=1
    [[ -f "$ROOT/.cursor/rules/switches.mdc" ]] || e_missing+=(".cursor/rules/switches.mdc")
fi
# 组间配对（裁定 1「部分在场即红」的整组缺半边；审查083-逻辑 MUST-FIX 修项）：
# agents 与 skills 互为配对，一在而另一整组缺即半身不遂；
# switches 单独在场而两组架构全无，同罪。整组缺与件缺同列 e_missing。
if (( e_agents_on != e_skills_on )); then
    (( e_agents_on == 0 )) && e_missing+=("agents/（整组缺）")
    (( e_skills_on == 0 )) && e_missing+=("skills/（整组缺）")
fi
if (( e_sw_on == 1 && e_agents_on == 0 && e_skills_on == 0 )); then
    e_missing+=("agents/（整组缺）" "skills/（整组缺）")
fi
e_present=()
(( e_agents_on )) && e_present+=("agents")
(( e_skills_on )) && e_present+=("skills")
(( e_sw_on )) && e_present+=("switches")
printf '== E 架构执行（在场性 v1，量程跟档位——5.20，PROMPT_083） ==\n'
if (( e_agents_on == 0 && e_skills_on == 0 && e_sw_on == 0 )); then
    warn "E 架构执行：轻档无执行架构，起步闸不适用（明记在案）"
elif (( ${#e_missing[@]} != 0 )); then
    fail "E 架构执行：半身不遂——开工即红（后补九标本）：缺 ${e_missing[*]}"
else
    pass "E 架构执行：在场配对齐（在场组：${e_present[*]}）——在场性 v1：生效性深检待 hooks 等实件出现"
fi

if (( fail_count != 0 )); then
    printf 'FAILED\n'
    exit 1
fi
printf 'ALL PASS\n'
