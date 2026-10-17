#!/usr/bin/env bash
# check-card.sh —— 卡审前机检三件（todo 5.52，cmd/PROMPT_107，2026-10-12）。
# 用法：bash tools/check-card.sh [--host-root HOST] [卡片路径]
# 不给参数时，从 SESSION.md 横线以上取当前卡。
# 只读卡面与 todo 案卷；不进 run.sh，也不把任何读数写成「通过」。
# 三条：
#   ①行位逐字：卡面 TODO 行号/短题逐字对到 todo 现行或档案行；
#   ③判据可机验：验收表每行有反引号命令，bash 语法可过，入口可执行；
#   ⑥先例一致：按卡面关键词列同族行索引；这一条只供审卡手参照，不代作语义判断。
set -u
export LC_ALL=C.UTF-8
SOURCE_ROOT=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)
SCRIPT="$SOURCE_ROOT/tools/check-card.sh"
CALLER_ROOT=$PWD
HOST_ROOT=$SOURCE_ROOT
if [ "$(basename "$SOURCE_ROOT")" = "src" ] && [ -f "$SOURCE_ROOT/../tests/test_layout.py" ]; then
  HOST_ROOT=$(cd "$SOURCE_ROOT/.." && pwd)
elif [ "$(basename "$(dirname "$SOURCE_ROOT")")" = "submodules" ]; then
  HOST_ROOT=$(cd "$SOURCE_ROOT/../.." && pwd)
fi
if [ "${1:-}" = "--host-root" ]; then
  if [ "$#" -lt 2 ] || [ ! -d "$2" ]; then
    echo "G0: FAIL --host-root 缺有效宿主目录"; exit 1
  fi
  HOST_ROOT=$(cd "$2" && pwd)
  shift 2
fi
if [ "$#" -eq 1 ] && [ -f "$1" ]; then
  CARD_ARG=$(cd "$(dirname "$1")" && pwd)/$(basename "$1")
else
  CARD_ARG=${1:-}
fi
cd "$HOST_ROOT" || exit 1

fail=0
TAB=$(printf '\t')

if ! bash -n "$SCRIPT"; then
  echo "G0: FAIL 脚本语法红"
  exit 1
fi

if [ "$#" -gt 1 ]; then
  echo "用法：bash tools/check-card.sh [--host-root HOST] [卡片路径]"
  exit 1
fi

if [ "$#" -eq 1 ]; then
  CARD=$CARD_ARG
else
  SESS=docs/SESSION.md
  if [ ! -f "$SESS" ]; then
    echo "G0: FAIL SESSION.md 不存在，且未给定卡片路径"
    exit 1
  fi
  CARD_REL=$(awk '/^---$/{exit} {print}' "$SESS" | grep -oE 'cmd/PROMPT_[0-9]{3,}\.md' | head -n1)
  if [ -z "$CARD_REL" ]; then
    echo "G0: FAIL SESSION 横线以上无卡面指针"
    exit 1
  fi
  CARD="docs/$CARD_REL"
fi
if [ ! -f "$CARD" ]; then
  echo "G0: FAIL 卡不存在：$CARD"
  exit 1
fi
echo "G0: 语法绿；卡=$CARD"

TODO_FILES=(docs/TODO.md)
for f in docs/archives/todo-*.md; do
  [ -f "$f" ] && TODO_FILES+=("$f")
done

# ---------- ① 行位逐字 ----------
echo
echo "== ① 行位逐字：卡面 TODO 行位 ↔ todo 现行/档案 =="
c1=0
META=$(grep -F '| **本刀是 TODO 哪一行** |' "$CARD" | head -n1)
ROW=$(printf '%s\n' "$META" | grep -oE '[0-9]+\.[0-9]+[a-z]*' | head -n1)
ROW=${ROW:-}
if [ -z "$META" ] || [ -z "$ROW" ]; then
  echo "   FAIL: 卡面抓不到「本刀是 TODO 哪一行」或行号"
  c1=1
else
  ROW_ESC=$(printf '%s\n' "$ROW" | sed 's/\./\\./g')
  ROWS=$(grep -hE "^- \[[ xX]\] \*\*$ROW_ESC\*\*" "${TODO_FILES[@]}")
  ROW_N=$(printf '%s' "$ROWS" | grep -c .)
  if [ "$ROW_N" -ne 1 ]; then
    echo "   FAIL: todo 并集行 $ROW 命中 $ROW_N 条（应为 1）"
    if [ -n "$ROWS" ]; then printf '%s\n' "$ROWS" | sed 's/^/      /'; fi
    c1=1
  else
    ROW_LINE=$(printf '%s\n' "$ROWS" | head -n1)
    ROW_TITLE=$(printf '%s\n' "$ROW_LINE" | sed -E 's/^- \[[ xX]\] \*\*[^*]+\*\*[[:space:]]*//' | sed -E 's/[（(:：].*$//')
    if [ -z "$ROW_TITLE" ]; then
      echo "   FAIL: 源行抓不到可核短题"
      c1=1
    elif ! printf '%s\n' "$META" | grep -Fq "\`$ROW\`"; then
      echo "   FAIL: 卡面行号未以反引号逐字写出：$ROW"
      c1=1
    elif ! grep -Fq -- "$ROW_TITLE" "$CARD"; then
      echo "   FAIL: 卡面未见源行短题：$ROW_TITLE"
      c1=1
    else
      echo "   PASS: 行 $ROW 唯一；短题逐字命中：$ROW_TITLE"
    fi
  fi
fi
[ "$c1" -eq 0 ] || fail=1

# ---------- ③ 判据可机验 ----------
echo
echo "== ③ 判据可机验：验收表逐格查命令 =="
c3=0
CANDIDATES=$(awk '
  function trim(s) { gsub(/^[[:space:]]+|[[:space:]]+$/, "", s); return s }
  function cellat(line, n,   c, i, cell, ci) {
    cell=""; ci=1
    for (i=1; i<=length(line); i++) {
      c=substr(line, i, 1)
      if (c == "\\" && substr(line, i+1, 1) == "|") { cell = cell "\\|"; i++; continue }
      if (c == "|") { if (ci == n) return cell; ci++; cell=""; continue }
      cell = cell c
    }
    return (ci == n ? cell : "")
  }
  /^## 验收命令/ { in_accept=1; next }
  in_accept && /^## / { exit }
  in_accept && /^\|/ {
    no=trim(cellat($0, 2)); cmd=trim(cellat($0, 3))
    if (no ~ /^[0-9]+$/) printf "%s\t%s\n", no, cmd
  }
' "$CARD")
ACCEPT_N=$(printf '%s' "$CANDIDATES" | grep -c .)
if [ "$ACCEPT_N" -eq 0 ]; then
  echo "   FAIL: 验收表抓不到数据行"
  c3=1
else
  while IFS="$TAB" read -r no cmd; do
    snippet=$(printf '%s\n' "$cmd" | grep -oE '`[^`]+`' | sed -e 's/^`//' -e 's/`$//' | head -n1)
    if [ -z "$snippet" ]; then
      echo "   FAIL: 格 $no 命令格无反引号命令：${cmd:-空}"
      c3=1
      continue
    fi
    if ! bash -n -c "$snippet"; then
      echo "   FAIL: 格 $no bash 语法红：$snippet"
      c3=1
      continue
    fi
    first=$(printf '%s\n' "$snippet" | sed -E 's/^[[:space:]]+//; s/^[[:space:]]*env[[:space:]]+//; s/[|&;].*$//')
    entry=${first%% *}
    if [ -z "$entry" ] || ! command -v "$entry" >/dev/null 2>&1; then
      echo "   FAIL: 格 $no 入口不在 PATH：${entry:-空}"
      c3=1
      continue
    fi
    case "$entry" in
      bash|sh)
        target=${first#* }
        target=${target%% *}
        if [ ! -f "$target" ]; then
          echo "   FAIL: 格 $no 脚本不存在：$target"
          c3=1
          continue
        fi
        if ! bash -n "$target"; then
          echo "   FAIL: 格 $no 目标脚本语法红：$target"
          c3=1
          continue
        fi
        ;;
      rg)
        rg --version >/dev/null 2>&1 || { echo "   FAIL: rg --version 不可跑"; c3=1; continue; }
        ;;
    esac
    echo "   PASS: 格 $no 命令在场、语法绿、入口可执行"
  done < <(printf '%s\n' "$CANDIDATES")
fi
[ "$c3" -eq 0 ] || fail=1

# ---------- ⑥ 先例一致：只建索引，不代作语义判断 ----------
echo
echo "== ⑥ 先例一致：按卡面关键词列同族行索引 =="
KEYWORDS=""
for kw in 审卡 写卡 闸一 角色 权限 检查 清单 判据 机检 先例 退卡; do
  grep -qF -- "$kw" "$CARD" && KEYWORDS="$KEYWORDS $kw"
done
KEYWORDS=${KEYWORDS# }
if [ -z "$KEYWORDS" ]; then
  echo "   FAIL: 卡面抓不到可检索关键词"
  fail=1
else
  echo "   关键词：$KEYWORDS"
  INDEX=$(for f in "${TODO_FILES[@]}"; do
    awk '/^- \[[ xX]\]/ { print FNR "\t" $0 }' "$f" |
    while IFS="$TAB" read -r line_no line; do
      case "$line" in *"$ROW"*) continue ;; esac
      score=0
      hits=""
      for kw in $KEYWORDS; do
        case "$line" in *"$kw"*) score=$((score + 1)); hits="${hits}${kw}、" ;; esac
      done
      if [ "$score" -gt 0 ]; then printf '%d\t%s:%s\t%s\t%s\n' "$score" "$f" "$line_no" "$hits" "$line"; fi
    done
  done)
  INDEX_N=$(printf '%s' "$INDEX" | grep -c .)
  if [ "$INDEX_N" -eq 0 ]; then
    echo "   INDEX: 零命中；是否新族留给审卡手判断"
  else
    echo "   INDEX: 命中 $INDEX_N 条，取前 8 条（按关键词重合数降序）"
    printf '%s\n' "$INDEX" | sort -nr | head -n8 | awk -F '\t' '{ if (length($5) > 240) $5=substr($5,1,240) "…"; OFS="\t"; print "      " $0 }'
    echo "   边界：本段只列先例，不裁「是否一致」；语义判断归审卡手"
  fi
fi

echo
if [ "$fail" -eq 0 ]; then
  echo "ALL PASS"
else
  echo "FAILED"
fi
exit "$fail"
