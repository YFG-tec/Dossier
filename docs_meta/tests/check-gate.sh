#!/usr/bin/env bash
# 版次连号、条目数、节名形状验收。零权威，只作证，不当运行入口。
# 用法：bash docs_meta/tests/check-gate.sh
#
# 谁加的：2026-09-13 由 SESSION.md 里的卡片指针新增，`contract-tester` 这只手写的。
# **这是收紧，不是放宽**，所以不另发一次授权（paradigm.md §3 第 4 条：松判据才是人的那一爪）。
# 同 check-link.sh C / D 两段、check-word.sh 整本那条理由。
#
# 为什么要有这一本：冻结点挪到结案，每刀开工后会回来重提红印，
# 导致版本号有可能不连号、某一版会有多行。
# 这一本来守卡上写的版本信息是不是跟真实发生的一致——
# 数不出内容对不对，但能数出形状有没有对上。
#
# 三段断言：
#
#   A 版次连号无缺 —— 横线以上「闸一红印」行，版次从 1 到 v 连号无缺，最大版次恰好一行。
#     版本号格式「第 N 版」的形状本本守。v = 1 时只检查有一行；v = 2 时检查有第 1、2 版各一行；以此类推。
#     D 段（check-link.sh）的职责让出去了，现在只检查形状，不检查数量。
#
#   B 条目数对 —— v ≥ 2 时，被指的卡里必须有「## 闸一之后动过的」那一节，
#     且该节底下的条目数恰好 = v − 1。
#     条目取法：节底下行首是 `- ` 的行（只增不删的清单）。数到下一个 `## ` 为止。
#     **取法写死成「行首 `## ` 之后逐字是节名」这一形，不许全文 `grep`**。
#     （正是这一条，`PROMPT_017` 整张退卡就死在这里）
#
#   C 节名有无 —— v = 1 时，那张卡里不许有「## 闸一之后动过的」节（没改过就不该有痕）。
#     **取法同 B，行首 `## ` 之后逐字是节名**。
#
#   v = 0 是写卡阶段，A / B / C 一律照红，那是设计，不是故障。脚本同 check-link.sh D 段做法，红就是红。
#
# **射程：从 SESSION.md 横线以上现算出本刀指向的卡（恰好一处），只看那一份，不含历史卡。**
#   历史卡带着旧形状的红印和旧节名，扫进来必假红。
#
# **脚本不写「这是第几本」。** 号脱钩另开一行（人 2026-09-13 裁），本数不在脚本头。
#
cd "$(dirname "$0")/../.."

fail=0
S=docs_meta/docs/SESSION.md

[ -f "$S" ] || { echo "FAIL: $S 不存在"; exit 1; }

# 横线以上 = 写卡那只手的那半页（同 check-link.sh 射程）
TOP=$(mktemp)
trap 'rm -f "$TOP"' EXIT
awk '/^---$/{exit} {print}' "$S" > "$TOP"

# 从 SESSION.md 现算卡号（恰好一处）
CARD_OCC=$(grep -oE 'cmd/PROMPT_[0-9]{3,}\.md' "$TOP" | wc -l)
if [ "$CARD_OCC" -ne 1 ]; then
  if [ "$CARD_OCC" -eq 0 ]; then
    echo "FAIL: SESSION.md 横线以上找不到卡片指针"
  else
    echo "FAIL: 卡片指针应为恰好一处，现 $CARD_OCC 处"
  fi
  exit 1
fi
CARD=$(grep -oE 'cmd/PROMPT_[0-9]{3,}\.md' "$TOP")
CARD="docs_meta/docs/$CARD"
[ -f "$CARD" ] || { echo "FAIL: $CARD 不存在"; exit 1; }

echo "（射程：SESSION.md 横线以上 $(wc -l < "$TOP") 行；现算指向 $CARD）"
echo

echo "== A 版次连号无缺，最大版次恰好一行 =="
# 从「闸一红印」行提取所有版次号
versions=$(grep '闸一红印' "$TOP" | grep -oE '第 [0-9]+ 版' | grep -oE '[0-9]+' | sort -n)
if [ -z "$versions" ]; then
  echo "   FAIL: 找不到『闸一红印』行"
  fail=1
else
  v=$(printf '%s\n' "$versions" | tail -1)
  echo "   版本范围: 1 ~ $v"

  # 检查版次是否连号
  expected_seq=$(seq 1 "$v" | paste -sd ' ')
  actual_seq=$(printf '%s\n' "$versions" | paste -sd ' ')
  if [ "$expected_seq" = "$actual_seq" ]; then
    echo "   PASS: 版次 $actual_seq 连号无缺"
  else
    echo "   FAIL: 版次不连号。期望 $expected_seq，实际 $actual_seq"
    fail=1
  fi

  # 检查最大版次是否恰好一行
  max_count=$(grep '闸一红印' "$TOP" | grep "第 $v 版" | wc -l)
  if [ "$max_count" -eq 1 ]; then
    echo "   PASS: 最大版次『第 $v 版』恰好一行"
  else
    echo "   FAIL: 最大版次『第 $v 版』出现 $max_count 行（应为 1）"
    fail=1
  fi
fi

echo
v=$(grep '闸一红印' "$TOP" | grep -oE '第 [0-9]+ 版' | grep -oE '[0-9]+' | tail -1)
if [ -z "$v" ]; then
  v=0
fi

if [ "$v" -ge 2 ]; then
  echo "== B v≥2：卡上必须有『## 闸一之后动过的』，条目数 n = v−1 =="
  if [ "$(grep -c '^## 闸一之后动过的$' "$CARD")" -eq 1 ]; then
    # 条目取法：节底下行首是 `- ` 的行（只增不删的清单）
    n=$(awk '/^## 闸一之后动过的$/{f=1; next} /^## /{f=0} f{if(/^- /)c++} END{print c+0}' "$CARD")
    expected=$((v - 1))
    if [ "$n" -eq "$expected" ]; then
      echo "   PASS: 条目数 $n = v−1"
    else
      echo "   FAIL: 条目数 $n（应为 $expected = $v−1）"
      fail=1
    fi
  else
    echo "   FAIL: 卡上找不到『## 闸一之后动过的』节（或找到多个）"
    fail=1
  fi
elif [ "$v" -eq 1 ]; then
  echo "== B 跳过：v=1，本段不适用 =="
elif [ "$v" -eq 0 ]; then
  echo "== B v=0 写卡阶段：照红是设计 =="
  echo "   FAIL: 写卡还没定"
  fail=1
fi

echo
if [ "$v" -eq 1 ]; then
  echo "== C v=1：卡上不许有『## 闸一之后动过的』 =="
  if grep -q '^## 闸一之后动过的$' "$CARD"; then
    echo "   FAIL: 卡上找到『## 闸一之后动过的』（v=1 不该有）"
    fail=1
  else
    echo "   PASS: 卡上没有『## 闸一之后动过的』"
  fi
elif [ "$v" -eq 0 ]; then
  echo "== C v=0 写卡阶段：照红是设计，不是故障 =="
  if grep -q '^## 闸一之后动过的$' "$CARD"; then
    echo "   FAIL: 卡上有『## 闸一之后动过的』（写卡还没定）"
  else
    echo "   FAIL: 卡上没有『## 闸一之后动过的』（写卡还没定）"
  fi
  fail=1
else
  echo "== C 跳过：v = $v ≠ 0、1 =="
fi

echo
if [ "$fail" -eq 0 ]; then
  echo "ALL PASS"
else
  echo "FAILED"
fi
exit "$fail"
