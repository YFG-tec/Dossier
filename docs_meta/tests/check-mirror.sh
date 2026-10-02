#!/usr/bin/env bash
# 副本骨架验收：`.mirror/` 那棵树是不是母本 harness 按一般项目形状转译出来的样子。零权威，只作证，不算「通过」。
# 用法：bash docs_meta/tests/check-mirror.sh
#
# 谁加的：2026-09-17 由 cmd/PROMPT_029.md 新增，契约测试这只手写的。
# **这是收紧，不是放宽**，不另发一次授权（roles.md：收紧是测试那只手的本职）。
#
# 为什么要有这一本：2.10a 交了 `.mirror/` 副本，母本 harness 人工转译到一般项目的形状。
#   这一本补的是人裁甲第一格——副本里 `docs_meta` 为 0 的独立功能检查，加副本自己的形状（11 件、占位符一种、host.md 不进、LF、空占位数）。
#   母本和副本对不对得上，本刀不管；那是 2.10c，派四本检查脚本。
#
# 钉的是哪几裁：
#   **期望值不从 init.py 里取，从卡上写死**（verify.md 第一条：同源同义反复）。
#   11 件清单逐件写在脚本里：出处是 cmd/PROMPT_029.md 第 2 件那张清单和 todo.md 2.10a 那一行。
#   六段断言和读数钉在 PROMPT_029.md「验收命令」第一组、第二组。
#   **期望值不从核里取，这一条对六段都成立。**
#
# 它查不到什么，照写不吹：
#   **只管副本自己的形状，不管副本和母本对不对得上。** 对得上的结构验收是 2.10c，那一本跑四本检查脚本。
#   母本加了一条禁令、副本没跟上，本刀不会红（庚没牙，缺口一）。
#   **这一本自己没有哨兵。** 断言写反了不会有东西红，只有人眼。
#
# 口径（脚本和文档必须同一套）：
#   扫射程：只扫 `.mirror/`，以仓库根下的 `.mirror` 为根。
#   不带根目录开关；`run.sh` 按 `docs_meta/tests/check-*.sh` 自动发现，会成为第十六本。
#   带中文和反引号的探针一律 `grep -F` 或 `grep -c` 字面，不用正则。
#   脚本末尾成功印 `ALL PASS`、失败印 `FAILED`，退出码 0 / 1。
#   CR 那个字节先赋给变量再进 $( )：这台 bash 在命令替换里会把 $'\r' 吃成空串，空模式全匹配，伪红。

set -e

MIRROR_ROOT=".mirror"
EXIT_CODE=0

# ============================================================================
# A 段：11 件逐件在，且 find .mirror -type f 恰好 11 件
# ============================================================================

echo "== A 11 件逐件在 =="

# 11 件清单，出处：cmd/PROMPT_029.md 第 2 件 + todo.md 2.10a
EXPECTED_FILES=(
  ".mirror/CLAUDE.md"
  ".mirror/AGENTS.md"
  ".mirror/.claude/agents/builder.md"
  ".mirror/.claude/agents/contract-tester.md"
  ".mirror/.claude/agents/review.md"
  ".mirror/.claude/agents/spec-guard.md"
  ".mirror/.claude/skills/write-cmd/SKILL.md"
  ".mirror/.claude/skills/one-slice/SKILL.md"
  ".mirror/.claude/skills/example-report/SKILL.md"
  ".mirror/.claude/settings.json"
  ".mirror/.cursor/rules/switches.mdc"
)

A_PASS=true

# 检查 11 件逐件在
for file in "${EXPECTED_FILES[@]}"; do
  if [ ! -f "$file" ]; then
    echo "   FAIL: 缺文件 $file"
    A_PASS=false
    EXIT_CODE=1
  fi
done

# 检查 find .mirror -type f 恰好 11 件
FILE_COUNT=$(find "$MIRROR_ROOT" -type f 2>/dev/null | wc -l)
if [ "$FILE_COUNT" -ne 11 ]; then
  echo "   FAIL: 副本里 find .mirror -type f 共 $FILE_COUNT 件，期望 11"
  A_PASS=false
  EXIT_CODE=1
fi

if [ "$A_PASS" = true ]; then
  echo "   PASS: 11 件逐件在，文件总数恰好 11"
else
  EXIT_CODE=1
fi

# 如果 .mirror/ 不在，跳过 B–F
if [ ! -d "$MIRROR_ROOT" ]; then
  echo "   跳过 B–F：.mirror/ 不在，先红"
  echo "FAILED"
  exit 1
fi

# ============================================================================
# B 段：`.mirror/` 里 docs_meta 0 处
# ============================================================================

echo "== B docs_meta 0 处 =="
B_PASS=true
DOCS_META_COUNT=$(grep -rl docs_meta "$MIRROR_ROOT" 2>/dev/null | wc -l)
if [ "$DOCS_META_COUNT" -ne 0 ]; then
  echo "   FAIL: 副本里 docs_meta 出现 $DOCS_META_COUNT 处，期望 0"
  B_PASS=false
  EXIT_CODE=1
fi

if [ "$B_PASS" = true ]; then
  echo "   PASS: docs_meta 0 处"
fi

# ============================================================================
# C 段：双花括号只有一种形状 {{DOSSIER_SRC}}，且至少 1 处
# ============================================================================

echo "== C 占位符只有 {{DOSSIER_SRC}} 一种 =="
C_PASS=true

# 检查双花括号只有一种形状
BRACKET_TYPES=$(grep -rho '{{[^}]*}}' "$MIRROR_ROOT" 2>/dev/null | sort -u | wc -l)
if [ "$BRACKET_TYPES" -ne 1 ]; then
  echo "   FAIL: 副本里有 $BRACKET_TYPES 种双花括号形状，期望 1 种"
  C_PASS=false
  EXIT_CODE=1
fi

# 检查这一种是 {{DOSSIER_SRC}}
BRACKET_TYPE=$(grep -rho '{{[^}]*}}' "$MIRROR_ROOT" 2>/dev/null | sort -u | head -1)
if [ "$BRACKET_TYPE" != "{{DOSSIER_SRC}}" ]; then
  echo "   FAIL: 双花括号唯一形状是 $BRACKET_TYPE，期望 {{DOSSIER_SRC}}"
  C_PASS=false
  EXIT_CODE=1
fi

# 检查至少 1 处 {{DOSSIER_SRC}}/
DOSSIER_SRC_COUNT=$(grep -rhoF '{{DOSSIER_SRC}}/' "$MIRROR_ROOT" 2>/dev/null | wc -l)
if [ "$DOSSIER_SRC_COUNT" -lt 1 ]; then
  echo "   FAIL: 副本里 {{DOSSIER_SRC}}/ 共 $DOSSIER_SRC_COUNT 处，期望至少 1"
  C_PASS=false
  EXIT_CODE=1
fi

if [ "$C_PASS" = true ]; then
  echo "   PASS: 占位符只有 {{DOSSIER_SRC}} 一种，共 $DOSSIER_SRC_COUNT 处"
fi

# ============================================================================
# D 段：`.mirror/.claude/host.md` 不在
# ============================================================================

echo "== D host.md 不进副本 =="
D_PASS=true
if [ -e "$MIRROR_ROOT/.claude/host.md" ]; then
  echo "   FAIL: .mirror/.claude/host.md 存在，期望不存在"
  D_PASS=false
  EXIT_CODE=1
fi

if [ "$D_PASS" = true ]; then
  echo "   PASS: .mirror/.claude/host.md 不存在"
fi

# ============================================================================
# E 段：`.mirror/` 里 CR 字节 0
# ============================================================================

echo "== E LF 行尾（量库内 blob 形，不量工作树——6.25 换尺，041/6.11 同族）=="
#   旧尺 grep -rlU $CR 数工作树含 CR 的文件：库内全是 LF，但 autocrlf 的 clone
#   把副本 smudge 成 CRLF → fresh clone 首跑恒红（假红）。断言要的是库里的事实，
#   尺子就得读库：git ls-files --eol 看 index 形，工作树 w/ 归环境，不管。
E_PASS=true
eol_lines=$(git ls-files --eol -- "$MIRROR_ROOT")
eol_n=$(printf '%s\n' "$eol_lines" | grep -c 'i/lf')
eol_all=$(printf '%s\n' "$eol_lines" | grep -c '^i/')
if [ "$eol_all" -ne 11 ]; then
  echo "   FAIL: .mirror 在库内只数到 $eol_all 件，期望 11——文件没入库？"
  E_PASS=false
  EXIT_CODE=1
elif [ "$eol_n" -ne "$eol_all" ]; then
  echo "   FAIL: 库内 $eol_all 件里有 $((eol_all-eol_n)) 件不是 i/lf——副本必须 LF 入库（autocrlf 管不着库）"
  E_PASS=false
  EXIT_CODE=1
fi

if [ "$E_PASS" = true ]; then
  echo "   PASS: 11 件全 i/lf（库内 blob 形；工作树被 smudge 成什么不算账）"
fi

# ============================================================================
# F 段：「空占位」在 `.mirror/CLAUDE.md` 恰好 2 行、`.mirror/AGENTS.md` 恰好 1 行
# ============================================================================

echo "== F 课题占位符数 =="
F_PASS=true

if [ -f "$MIRROR_ROOT/CLAUDE.md" ]; then
  CLAUDE_PLACEHOLDER=$(grep -c 空占位 "$MIRROR_ROOT/CLAUDE.md" || true)
  if [ "$CLAUDE_PLACEHOLDER" -ne 2 ]; then
    echo "   FAIL: .mirror/CLAUDE.md 里「空占位」共 $CLAUDE_PLACEHOLDER 行，期望 2"
    F_PASS=false
    EXIT_CODE=1
  fi
else
  echo "   FAIL: .mirror/CLAUDE.md 不存在"
  F_PASS=false
  EXIT_CODE=1
fi

if [ -f "$MIRROR_ROOT/AGENTS.md" ]; then
  AGENTS_PLACEHOLDER=$(grep -c 空占位 "$MIRROR_ROOT/AGENTS.md" || true)
  if [ "$AGENTS_PLACEHOLDER" -ne 1 ]; then
    echo "   FAIL: .mirror/AGENTS.md 里「空占位」共 $AGENTS_PLACEHOLDER 行，期望 1"
    F_PASS=false
    EXIT_CODE=1
  fi
else
  echo "   FAIL: .mirror/AGENTS.md 不存在"
  F_PASS=false
  EXIT_CODE=1
fi

if [ "$F_PASS" = true ]; then
  echo "   PASS: 空占位数恰好"
fi

# ============================================================================
# 总结
# ============================================================================

if [ "$EXIT_CODE" -eq 0 ]; then
  echo "ALL PASS"
else
  echo "FAILED"
fi

exit "$EXIT_CODE"
