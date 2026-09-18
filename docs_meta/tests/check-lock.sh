#!/usr/bin/env bash
# 根上那两份约定层锁的绊线。零权威，只作证，不算「通过」。
# 用法：bash docs_meta/tests/check-lock.sh
#
# 谁加的：2026-09-10 由 cmd/PROMPT_011.md 新增，实现席这只手写的。
# **这是收紧，不是放宽**，所以不另发一次授权（paradigm.md §3 第 4 条：松判据才是人的那一爪）。
# 同 check-word.sh 整本、check-link.sh C / D 两段、check-seat.sh 整本那条理由。
#
# 为什么要有第九本：原有八本的射程里，根 CLAUDE.md / AGENTS.md 一份都不在。
#   check-paw 扫 paradigm.md，check-done 扫 todo.md 加 cmd/，check-mark 扫 workflow.md，
#   check-cmd 扫 src/ 那几份加 paradigm.md，check-rename 扫 readme.md 加 src/ 加两张图，
#   check-link 扫 SESSION.md，check-seat 扫 roles.md，check-word A 段扫 src/ 加 readme.md。
#   具体后果：产物里写了作废的旧词没有东西会红，两份锁同时消失也没有东西会红。
#
# 钉的是哪几裁：
#   **约定层落 CLAUDE.md / AGENTS.md 两份**（todo.md 2.4 那一行）。
#   **同一份锁写短的**（claude-code.md 12–13、cursor.md 12、directory.md 97–98）——
#     本刀把「短的」落成指针，不落成摘要。摘要和正本迟早不一致，
#     不一致时没人知道该信哪个，那正是 xenia.md 第 4 节第 4 条那个洞。
#   **四个词定死**（人 2026-09-10）：审卡 / 闸一 / 验收 / 结案。「闸二」作废。
#   **不能两处都留**（todo.md 2.4 那一行原文）——ch2.md 第 0 节是 CLAUDE.md 的代偿，
#     约定层一落它就得迁走，两处都留就是同一批禁令抄了两份。
#
# 口径（脚本和文档必须同一套）：
#
#   A 两份都在 —— 根 CLAUDE.md 和 AGENTS.md 都必须存在。少一份就红。
#     约定层空着的时候这一条是红的，那是本刀开工前的正常态。
#
#   B 短的那份是指针 —— AGENTS.md 里必须出现 CLAUDE.md 这个词。
#     指针一没，短锁就退化成孤立的摘要，正是上面那个洞。
#     **它查得了指针在不在，查不了指针后面那份是不是真的被读了。**
#
#   C 旧词没进产物 —— CLAUDE.md 加 AGENTS.md 里「闸二」出现 0 次。
#     check-word 的 A 段只扫 docs_meta/src/ 加 readme.md，产物落在它射程之外。
#
#     **两份文件不在，C 算 PASS。** 它是绊线，不是待补项——
#     「文件还没落」本来就该由 A 去红，不该在 C 这里红第二次。
#     所以实现上先判文件在不在，不在就当 0 命中，不直接 grep 一个可能不在的文件
#     （grep 对不存在的文件退 2，壳会跟着红，那种红指的是「文件没落」，不是「旧词进了产物」）。
#     形状照 check-word.sh E 段那句「绊线不是待补项」写：
#     先红后绿那一次，C 是绿的；那一次它要是红的，先查是不是把「文件不在」写成了红。
#
#   D 退役（2026-09-12，人本回合点名「check-lock D：关闭硬依赖」）。原来查的是：
#     ch2.md 里「禁令（接收方）」必须 0 处——防第 0 节那一块和 CLAUDE.md 两处都留。
#     **退役理由**：这一条断言的对象是 `docs/design/ch2.md`，思路层。
#     `2.9` 把 `design/` 从红绿判定里剥出去之后，把关层再拿它当断言就是同一种用法，
#     和 E 段退役的理由是同一条。留着它，落地检查就仍然硬依赖 design。
#     退役是放宽，不是收紧，所以不能由测试这只手自己做（同 E 段、check-mark.sh A / B 的先例）。
#
#     **代价照写，不假装没损失**：「不能两处都留」现在没有哨兵。那九条被抄回 design 里去，
#     不会有东西变红，只能靠人读。**是少了一格，不是换了地方。**
#     真要补，哨兵得锚在 `docs_meta/src/` 或根上那两份产物上，不能再锚回 design。
#     那是另一刀，这里只留这一句，不在本处发明。
#
#   E 退役（2026-09-11，`cmd/PROMPT_013.md` 第 9 件）。原来查的是：paradigm.md 里
#     「还没落 `CLAUDE.md`」必须 0 处——防母本写着约定层空着、根上却躺着两份。
#     **退役理由**：那一刀把 `design/` 从红绿判定里剥出去，`paradigm.md` 整份降成思路层。
#     拿一份思路层的措辞当断言，正是这一刀要废掉的那种用法；留着它，本刀落完自相矛盾。
#     **人 2026-09-11 落槌**「字面退役」。退役是放宽，不是收紧，所以不能由测试这只手自己做
#     （同 check-mark.sh A / B 两段的先例）。
#
#     **代价照写，不假装没损失**：§9 那一行现在没有哨兵。它变假了也不会有东西变红，
#     只能靠人读。这一刀换来的是「不拿思路层当判据」，换掉的是这一格机械保险——
#     **是少了一格，不是换了地方。**
#
# **不设放行词。** 剩下三条一条都没留「同一行还出现某某就放过」的口子。
#   留了就等于说「提一句可以」，而「提一句」和「真写死」之间没有机器分得清的界
#   （同 check-link.sh A、check-word.sh 整本）。
#
# 副本内容检查用的根目录开关：环境变量 LOCK_ROOT，默认仓库根（不设时路径不前缀）。
#   **它是给副本用的：对副本做内容检查时，产物在副本，源码仍是母本那一份——本本只查产物，换根即可。**
#   造红也走这一路，破的是副本那一份，母本一个字不动——这是纪律，不是方便。
#   **run.sh 走默认那一路，不带参数、不设这个变量。**
#
# **它查不了什么，照写不吹：** 查得了两份文件在不在、几个词有没有落地，
#   **查不了 CLAUDE.md 里那些禁令是不是真能拦住手**
#   （paradigm.md §6：能机检的是词的共现，不是意思）。
#   三条全绿，那两份锁照样可以被写成一份漏了最关键几条的清单——只要它绕开这几个词。
#   拦得住手滑，拦不住漏写。**而「漏」正是 §9 那条偏离代价栏里写的、最可能的失效模式。**
#   本刀这一本自己就是那条偏离的第三条防线，同时也是同一只手写的，见 §9 代价第二条。
cd "$(dirname "$0")/../.."
fail=0
ROOT="${LOCK_ROOT:-}"
ROOT="${ROOT%/}"
C="${ROOT:+$ROOT/}CLAUDE.md"
A="${ROOT:+$ROOT/}AGENTS.md"

echo "（射程：根 $C / $A。D / E 两段已退役——见脚本头）"
echo

echo "== A 两份都在：根 CLAUDE.md 和 AGENTS.md 都必须存在 =="
echo "   （约定层空着时这一条红，那是本刀开工前的正常态）"
a=0
for f in "$C" "$A"; do
  if [ -f "$f" ]; then
    echo "   OK   $f 在"
  else
    echo "   BAD  $f 不在"
    a=1
  fi
done
if [ "$a" -eq 0 ]; then
  echo "   PASS: 两份都在"
else
  echo "   FAIL: 上面 BAD 那份没落——约定层还是空的"
  fail=1
fi

echo
echo "== B 短的那份是指针：AGENTS.md 里必须出现 CLAUDE.md =="
echo "   （指针一没，短锁就退化成孤立的摘要，那是同一条规矩抄两份的老洞）"
if [ ! -f "$A" ]; then
  echo "   FAIL: $A 不在，无从查指针（A 段已经报过一次）"
  fail=1
else
  hit=$(grep -n 'CLAUDE\.md' "$A")
  if [ -n "$hit" ]; then
    printf '%s\n' "$hit" | sed 's/^/   /'
    echo "   PASS: 指针在"
  else
    echo "   FAIL: $A 里没有 CLAUDE.md——短锁成了孤立的摘要"
    fail=1
  fi
fi

echo
echo "== C 旧词没进产物：CLAUDE.md 加 AGENTS.md 里「闸二」必须 0 处 =="
echo "   （两份都不在就算 PASS：绊线不是待补项，「文件还没落」由 A 段去红，不在这里红第二次）"
present=""
for f in "$C" "$A"; do
  [ -f "$f" ] && present="$present $f"
done
if [ -z "$present" ]; then
  echo "   （两份都不在，按口径当 0 命中）"
  echo "   PASS: 0 处"
else
  hit=$(grep -n '闸二' $present /dev/null)
  if [ -z "$hit" ]; then
    echo "   扫了：$present"
    echo "   PASS: 0 处，旧词没进产物"
  else
    printf '%s\n' "$hit" | sed 's/^/   /'
    echo "   FAIL: 还剩 $(printf '%s\n' "$hit" | wc -l) 处——「闸二」作废，一律换成「结案」"
    fail=1
  fi
fi

echo
if [ "$fail" -eq 0 ]; then
  echo "ALL PASS"
else
  echo "FAILED"
fi
exit "$fail"
