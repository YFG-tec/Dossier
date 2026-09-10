#!/usr/bin/env bash
# workflow.md「开桌」那一节的同步验收。零权威，只作证，不算「通过」。
# 用法：bash docs_meta/tests/check-mark.sh
#
# **文件名是历史。** 本脚本原来有三段：
#   A 裸标记的位置格式（paradigm.md / workflow.md）
#   B 越权：裸标记只许在 paradigm.md 的 §3 / §5 / §6 / §10，总数 ≤ 5
#   C workflow.md「开桌」那一节，机制和旧规矩都得改到
#
# **A 和 B 已于 2026-09-09 退役**，依 cmd/PROMPT_007.md（todo.md 2.1，人落槌「字面退役」）：
# 母本停用标记之后，A 守的是一个已经不存在的机制；B 的白名单和上限也没有对象了。
# **代价照写，不粉饰：** 退掉 B 之后，母本没有任何机械物拦得住第六个标记，
# 5 处冻住这件事只靠 paradigm.md 文首那一行字拦。这一条已记进 paradigm.md §9 的代价栏。
#
# **脚本头原来兼着一本账**（谁在哪一刀批过哪一节）——**已整本搬进 paradigm.md §9**，
# 这里一个字不留：留副本就是第二真相（§5「能从别处现算出来的，不存」）。
#
# **C 段一个字没动，也不随 A / B 走。** 它守的是 workflow.md 给桌的通则，
# 而桌的标记照用（管理类不用、业务类照用，见 workflow.md「标记只落在业务结论上」）。
# 文件名不改：改名是以后把稳定的检查搬进 tests/ 时顺手的事，那要另开一行。
#
# C 查不了什么，照写：它验的是词的共现，不是意思（paradigm.md §6）。
cd "$(dirname "$0")/../.."
fail=0
WF=docs_meta/src/workflow.md
MARK=$'【定】'

echo "== C 同步：workflow.md 三态那一节，机制和旧规矩都得改到 =="
sec=$(awk '/^## /{f = ($0 ~ /^## 开桌/)} f' "$WF")
for kw in $'默认不可引' "$MARK" $'写作建议'; do
  if printf '%s' "$sec" | grep -q "$kw"; then
    echo "   有「$kw」"
  else
    echo "   FAIL: 开桌那一节缺「$kw」"
    fail=1
  fi
done
old=$(grep -n $'问句' "$WF" | grep $'机械保险')
if [ -n "$old" ]; then
  echo "$old"
  echo "   FAIL: 上面这行还把「机械保险」挂在「问句」上——那条职责已经被顶掉了"
  fail=1
else
  echo "   「问句」不再自称机械保险，正确"
fi

# C4：审查点出上面三条只扫「开桌」那一节，扫不到全程图那一段。
# 这是**收紧**，不是放宽——收紧判据是测试那只手的本职，放宽才是挪门槛。
stale=$(grep -n $'第一刀要碰的' "$WF" | grep -v $'标' | grep -v $'授权')
if [ -n "$stale" ]; then
  echo "$stale"
  echo "   FAIL: 全文里还有「第一刀要碰的…」没换成授权口径（节 / 已定 是旧粒度）"
  fail=1
else
  echo "   全文「第一刀要碰的…」都已换成授权口径"
fi

echo
if [ "$fail" -eq 0 ]; then echo "ALL PASS"; else echo "FAILED"; fi
exit $fail
