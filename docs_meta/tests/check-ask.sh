#!/usr/bin/env bash
# 「要人点的请示」每条带不带途径附注的形状验收。零权威，只作证，不算「通过」，不当运行入口。
# 用法：bash docs_meta/tests/check-ask.sh
#       ASK_ROOT=某根 bash docs_meta/tests/check-ask.sh    （换根，形状同 check-lock.sh 的 LOCK_ROOT）
#
# 谁加的：`todo.md` 4.10，卡 cmd/PROMPT_037.md 第三件，contract-tester 这只手写的（2026-09-23）。
# **这是收紧，不是放宽**，所以不另发一次授权——收紧口径是测试这只手的本职（roles.md）；
# 放宽判据才是人的一爪，本本没做、也不许自己做那一爪。
#
# 断言口径（与卡第三件同一套）：
#
#   射程两段：
#     一、当前卡——从 SESSION.md 横线以上的 cmd/PROMPT_NNN.md 指针现算（恰好一处），
#        取法同 check-gate.sh；指针缺、多、指向不存在的文件，一律红，红因同 check-gate。
#     二、SESSION.md 横线以上本身（停报写在这里；横线以下是审阅，不在射程）。
#   每段找「^## 要人点的请示$」那一节：
#     节不存在 → 该段 PASS（这一刀没有请示）。节存在但无条目 → 也 PASS，空节没东西可查。
#     节存在：节内每条行首「- 」的条目行必须含 〔爪：、〔途径一：、〔途径二： 三者之一。
#       三个附注是**字面**，用 grep -F 匹配全角词，不当正则用；模式里没有反引号。
#       有一条不含 → FAIL，点名来源、行号、行内容。
#   **跨行条目只查首行**——附注跟着条目走，机器只认「- 」那一行；把附注挪到第二行会红。
#     这是口径，不是缺陷（卡第三件写死）。
#
# 它查不了什么，照写不吹：
#   一、**聊天级的请示看不见**。本本只查落了盘的条目；「该落盘而没落」没有机检（卡缺口一）。
#   二、**附注的真假不判，只判形状**。〔途径一：…〕里写一个站不住的理由，形状照样绿。
#       机检的是词的共现，不是意思（卡缺口二，与 check-cmd.sh 脚本头同一条边界）。
#   三、历史卡、历史 SESSION 不在射程——只增不删、回填不了，扫它们是造永远的红（卡缺口四）。
#
# 根开关 ASK_ROOT：默认不设 = 仓库根，行为与本刀落地前的默认路径完全一致。
#   换根是给红绿探针用的：探针在 .tmp/ 下造一棵假树（镜像 docs_meta/docs/ 的形状），
#   破的是假树那一份，真盘一个字不动——这是纪律，不是方便。run.sh 走默认那一路。
#
# 脚本不写「这是第几本」——本数由 run.sh 现数（人 2026-09-13 裁，同 check-gate.sh 末注）。
cd "$(dirname "$0")/../.."

fail=0
ROOT="${ASK_ROOT:-}"
ROOT="${ROOT%/}"
D="${ROOT:+$ROOT/}docs_meta/docs"
S="$D/SESSION.md"

[ -f "$S" ] || { echo "FAIL: $S 不存在"; exit 1; }

# 横线以上 = 写卡、施工那只手的那半页（同 check-gate.sh 的取法；行号与原文件一致）
TOP=$(mktemp)
trap 'rm -f "$TOP"' EXIT
awk '/^---$/{exit} {print}' "$S" > "$TOP"

CARD_OCC=$(grep -oE 'cmd/PROMPT_[0-9]{3,}\.md' "$TOP" | wc -l)
if [ "$CARD_OCC" -ne 1 ]; then
  if [ "$CARD_OCC" -eq 0 ]; then
    echo "FAIL: SESSION.md 横线以上找不到卡片指针"
  else
    echo "FAIL: 卡片指针应为恰好一处，现 $CARD_OCC 处"
  fi
  exit 1
fi
CARD="$D/$(grep -oE 'cmd/PROMPT_[0-9]{3,}\.md' "$TOP")"
[ -f "$CARD" ] || { echo "FAIL: $CARD 不存在"; exit 1; }

echo "（射程：根 ${ROOT:-仓库根默认}；当前卡 $CARD 现算自 $S 横线以上，另扫 $S 横线以上本身）"
echo

# scan 显示名 文件 —— 0 = 该段绿，1 = 该段红
scan() {
  local name="$1" file="$2"
  if [ "$(grep -c -E '^## 要人点的请示$' "$file")" -eq 0 ]; then
    echo "   PASS: $name 无「## 要人点的请示」节——这一刀没有请示"
    return 0
  fi
  local items ln txt total bad
  items=$(awk '/^## 要人点的请示$/{f=1; next} /^## /{f=0} f && /^- /{printf "%d\t%s\n", NR, $0}' "$file")
  if [ -z "$items" ]; then
    echo "   PASS: $name 节存在但无条目（行首 - 开头 0 条），没有请示可查"
    return 0
  fi
  total=0
  bad=0
  while IFS=$'\t' read -r ln txt; do
    [ -n "$ln" ] || continue
    total=$((total + 1))
    if ! printf '%s\n' "$txt" | grep -qF -e '〔爪：' -e '〔途径一：' -e '〔途径二：'; then
      echo "   FAIL: $name 第 $ln 行 条目无附注：$txt"
      bad=1
    fi
  done <<DATA
$items
DATA
  if [ "$bad" -eq 0 ]; then
    echo "   PASS: $name 节内 $total 条条目，条条带附注"
  fi
  return "$bad"
}

echo "== A 当前卡 =="
scan "$CARD" "$CARD" || fail=1
echo
echo "== B SESSION.md 横线以上本身 =="
scan "${S}（横线以上）" "$TOP" || fail=1

echo
if [ "$fail" -eq 0 ]; then
  echo "ALL PASS"
else
  echo "FAILED"
fi
exit "$fail"
