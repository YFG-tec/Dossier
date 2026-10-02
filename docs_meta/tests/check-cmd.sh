#!/usr/bin/env bash
# cmd/ 定位验收：它是在办层唯一只增不删的历史。零权威，只作证，不算「通过」。
# 用法：bash docs_meta/tests/check-cmd.sh
#
# 这三条查的是**词的共现，不是意思**。能抓「cmd 和覆盖出现在同一行而没说清区别」，
# 抓不到「整段读下来仍然把 cmd 说成会被覆盖」。边界写在这里，别拿它当把关层。
#
# A 段的扫描名单 2026-09-11 去掉了 `paradigm.md`（`cmd/PROMPT_013.md` 第 11 件）：
#   那一刀把 `design/` 从红绿判定里剥出去，不在思路层的文件上做机械断言。
#   **人 2026-09-11 落槌**「字面退役」。减扫描目标是放宽，不由测试这只手自己做。
#   **代价照写**：`paradigm.md` 里以后写出含混的行不会红。去掉它的那一刻盘上命中 0 处，
#   所以这一减没有掩盖任何现存问题；但往后漏了就只能靠人读。
# D 段 2026-09-25 新增（6.12/反馈#3）：权限表 cmd/SESSION 行的实现席格不许回到裸「只读」。
# A 段防词含混；D 段防这张表对 roles.md 的单边授权声明。加检查是收紧不是放宽（本手本职，不发授权）。
cd "$(dirname "$0")/../.."
# E 段 2026-09-25 新增（6.15/6.17/6.18 并修三件套/反馈#6#8#9）：立案三件套不许回退——
#   权限表须有 TODO.md 独立行（6.18 的「根本不在场」），全程图须有 ⓪ 立案格（6.15/6.17 的动作与入口）。
#   加检查是收紧不是放宽（本手本职，不发授权）。
fail=0
SRC="docs_meta/src/directory.md docs_meta/src/workflow.md \
     docs_meta/src/roles.md docs_meta/src/cursor.md"

echo "== A lint：一行里既提 cmd/PROMPT 又提「覆盖」，就必须说清 cmd 不被覆盖 =="
echo "   （放行条件：同一行还出现「只增」或「新增」）"
bad=$(grep -nE 'cmd|PROMPT' $SRC | grep $'覆盖' | grep -v $'只增' | grep -v $'新增')
if [ -n "$bad" ]; then
  echo "$bad"
  echo "   FAIL: 上面这些行把 cmd 和「覆盖」摆在一起，没区分"
  fail=1
else
  echo "   PASS: 没有含混的行"
fi

echo
echo "== B directory.md 六块表「在办」那一行须写全三种寿命 =="
row=$(grep -n '^| 在办 |' docs_meta/src/directory.md)
echo "   $row"
if echo "$row" | grep -q $'只增' && echo "$row" | grep -q $'覆盖'; then
  echo "   PASS: 「只增」和「覆盖」都在"
else
  echo "   FAIL: 寿命栏没写全（须同时出现「只增」和「覆盖」）"
  fail=1
fi

echo
echo "== C 三份主文档里「只增不删」各至少一次 =="
for f in docs_meta/src/directory.md docs_meta/src/workflow.md docs_meta/src/roles.md; do
  n=$(grep -c $'只增不删' "$f")
  echo "   $f  ->  $n"
  if [ "$n" -lt 1 ]; then echo "   FAIL: $f 没写"; fail=1; fi
done

echo
echo "== D directory.md 权限表 cmd/SESSION 行的实现席格不许裸只读（2026-09-25，6.12/反馈#3） =="
row=$(grep -n '其余（cmd / SESSION / reports）' docs_meta/src/directory.md)
if [ -z "$row" ]; then
  echo "   FAIL: 权限表里找不到那一行——表结构变了，先重新现算射程"
  fail=1
elif ! echo "$row" | grep -q '写卡' || ! echo "$row" | grep -q '由桌自己定'; then
  echo "   FAIL: 那一行的实现席格回到了裸「只读」——两处出处又会打架（roles.md write-cmd 行还在说新增+覆盖）"
  fail=1
else
  echo "   PASS: 实现席格带着写卡豁免"
fi

echo
echo "== E 立案三件套在盘（2026-09-25，6.15/6.17/6.18 并修/反馈#6#8#9） =="
trow=$(grep -c '^| `docs/TODO.md`' docs_meta/src/directory.md)
zero=$(grep -c '⓪' docs_meta/src/workflow.md)
if [ "$trow" -lt 1 ]; then
  echo "   FAIL: 权限表没有 TODO.md 独立行——6.18「根本不在场」的形状回来了"
  fail=1
elif [ "$zero" -lt 1 ]; then
  echo "   FAIL: 全程图没有 ⓪ 立案格——裂行/写行的动作从图上消失了"
  fail=1
else
  echo "   PASS: TODO 有行，立案有格"
fi

echo
if [ "$fail" -eq 0 ]; then echo "ALL PASS"; else echo "FAILED"; fi
exit $fail
