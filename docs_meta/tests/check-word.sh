#!/usr/bin/env bash
# 四个词改名 + 补卡这一节的绊线。零权威，只作证，不算「通过」。
# 用法：bash docs_meta/tests/check-word.sh
#
# 谁加的：2026-09-10 由 cmd/PROMPT_010.md 新增，实现席这只手写的。
# **这是收紧，不是放宽**，所以不另发一次授权（paradigm.md §3 第 4 条：松判据才是人的那一爪）。
# 同 check-link.sh C / D 两段、check-seat.sh 整本那条理由。
#
# 钉的是哪几裁：
#   **四个词定死**（人 2026-09-10）：审卡 / 闸一 / 验收 / 结案。「闸二」作废。
#   **补卡是纠错完善补充历史已完成卡的完整一刀**（人 2026-09-10）——对象是已经结案的那一刀，
#     不是往在办的卡上追加。**理由是一事一结，整个历史是清晰的**（人同一回合原话）。
#   **写卡草稿的时候，SESSION 同步更新**（人 2026-09-10 审卡当场加）——卡每改一稿，上半页跟一稿。
#
# 口径（脚本和文档必须同一套）：
#
#   A 旧词归零 —— docs_meta/src/ 加 readme.md 里「闸二」出现 0 次。有一处就红。
#
#     **只扫 *.md，不含 figures/，这是本刀自己收的射程，照写不吹。**
#     卡上第一条写的是「docs_meta/src/ 加 readme.md」。照字面扫全目录会扫到
#     figures/dossier-frame.svg，那里有一处 闸二「勾 TODO」——而人 2026-09-10 裁「图不管了」。
#     照字面实现，这一条要么永远红，要么逼实现去改图，两头都和那一裁反着。
#     只扫 *.md 之后正文那 13 处仍须归零，和待办行里写的射程一个数不差。
#     形状照 check-link.sh「只扫横线以上」那条射程写：**断言本身一个字没松，收的是射程。**
#     **这是本刀这只手的判断，不是人裁的。** 结案时若认为该照字面，改回来即可，另六条不受影响。
#
#     图那一处的代价照记，不因为人裁了就当它不存在：改完之后正文说「结案」、
#     首页那张图说「闸二」，库里确实同时活着新旧两套。
#
#   B 新词落地 —— workflow.md 必须同时出现「审卡」和「补卡」。缺一就红。
#     两个都是新立的词，盘上本来 0 处。只在别处用、不在通则里定义，当场红。
#
#   C 两爪没被捆回验收 —— workflow.md 里凡出现「验收」且同行出现「commit」或「勾」的行，
#     同行必须出现「结案」。
#     验收不含 commit 和勾，那两样在结案，是人的那一爪（paradigm.md §3 第 4 条）。
#     有人把它们写回验收那一段，当场红。
#
#   D 后门没被开 —— workflow.md 补卡那一节必须出现「松判据」。
#     「补卡不松判据」是四条边界里最容易掉的一条：补卡本来就是「再加点东西」的形状，
#     那一句一没，它就成了绕过判据的壳。照「退卡不是松判据的后门」那句的写法写。
#
#   E 冻结那一条没被松 —— workflow.md 必须恰好一处「许可面定在结案，结案之前退回闸一才改得动，改完要重提」。
#
#     **绊线，不是待补项。** 先红后绿那一次，E 是绿的；那一次它要是红的，说明脚本写反了。
#     钉它的理由：本刀第一版把补卡写成了往老卡上追加，为此第一件要松的就是这一句。
#     人一句话推翻了那一版。补卡若哪天被读回成追加，第一个动的还是它。
#     这条线 2026-09-13 重瞄过。旧锚点是「许可面定在闸一」；新锚点是上面那一串。
#     为什么这是重瞄不是拆：旧规矩下冻结点在闸一，新规矩下挪到结案；同一条判据换了表述位置和时点，但地位不变。
#
#   F 理由没被当成修辞删掉 —— workflow.md 必须出现「一事一结」。
#     那是补卡这一节的承重墙。理由一没，规矩就只剩手续，
#     而不带理由的规矩下一个人会当成税删掉（paradigm.md §10）。
#
#   G 跟稿那条时点没被删 —— workflow.md 必须出现「跟一稿」。
#     ② 那一段补的时点最像流程赘述，最容易被下一个人当成废话删。
#     它一没，审卡又会读到一份对不上的运行态——本刀自己就是那个现场。
#
# **不设放行词。** 七条一条都没留「同一行还出现某某就放过」的口子。
#   留了就等于说「提一句可以」，而「提一句」和「真写死」之间没有机器分得清的界（同 check-link.sh A）。
#
# **它查不了什么，照写不吹：** 查得了词在不在、哪几个词有没有落在同一行，
#   **查不了整段读下来是不是仍然说反了**（paradigm.md §6：能机检的是词的共现，不是意思）。
#   七条全绿，补卡那一节照样可以被写成「可以往在办的卡上加东西」——只要它绕开这几个词。
#   拦得住手滑，拦不住误解。人读那两条写在卡的「验收」栏里，机器替不了。
cd "$(dirname "$0")/../.."
fail=0
W=docs_meta/src/workflow.md

[ -f "$W" ] || { echo "FAIL: $W 不存在"; exit 1; }

# 取节：从 ^## <名> 到下一个 ^## 之前。带原文行号，报告时能点名。
section() {
  awk -v pat="$1" '
    $0 ~ "^## " pat { f=1; print NR"\t"$0; next }
    /^## / { f=0 }
    f { print NR"\t"$0 }
  ' "$W"
}

echo "（射程：A 扫 docs_meta/src/ + readme.md 的 *.md；B–G 扫 workflow.md——见脚本头）"
echo

echo "== A 旧词归零：src/ 加 readme.md 的 *.md 里「闸二」必须 0 处 =="
echo "   （不含 figures/：那一处是 .svg，人 2026-09-10 裁「图不管了」，射程理由见脚本头）"
hit=$(grep -rn --include=*.md '闸二' docs_meta/src/ readme.md)
if [ -z "$hit" ]; then
  echo "   PASS: 0 处，改名做完了"
else
  printf '%s\n' "$hit" | sed 's/^/   /'
  echo "   FAIL: 还剩 $(printf '%s\n' "$hit" | wc -l) 处——「闸二」作废，一律换成「结案」"
  fail=1
fi

echo
echo "== B 新词落地：workflow.md 必须同时出现「审卡」和「补卡」 =="
echo "   （两个都是新立的词，盘上本来 0 处；只在别处用、不在通则里定义，当场红）"
b=0
for w in 审卡 补卡; do
  n=$(grep -c "$w" "$W")
  if [ "$n" -gt 0 ]; then
    echo "   OK   「$w」 $n 处"
  else
    echo "   BAD  「$w」 0 处"
    b=1
  fi
done
if [ "$b" -eq 0 ]; then
  echo "   PASS: 两个词都在"
else
  echo "   FAIL: 上面 BAD 那个词没落进通则"
  fail=1
fi

echo
echo "== C 两爪没被捆回验收：含「验收」且含「commit」或「勾」的行，必须同行含「结案」 =="
echo "   （验收不含 commit 和勾，那两样在结案，是人的那一爪）"
lines=$(grep -n '验收' "$W" | grep 'commit\|勾')
if [ -z "$lines" ]; then
  echo "   （没有这样的行）"
  echo "   PASS: 没有把两爪写进验收的行"
else
  c=0
  while IFS= read -r l; do
    if printf '%s' "$l" | grep -q '结案'; then
      printf '   OK   %s\n' "$l"
    else
      printf '   BAD  %s\n' "$l"
      c=1
    fi
  done <<< "$lines"
  if [ "$c" -eq 0 ]; then
    echo "   PASS: 每一处都点着「结案」"
  else
    echo "   FAIL: 上面 BAD 那几行把 commit / 勾捆回了验收"
    fail=1
  fi
fi

echo
echo "== D 后门没被开：补卡那一节必须出现「松判据」 =="
echo "   （「补卡不松判据」是四条边界里最容易掉的一条）"
SUP=$(section '补卡')
if [ -z "$SUP" ]; then
  echo "   FAIL: workflow.md 里找不到 '## 补卡' 那一节"
  fail=1
else
  hit=$(printf '%s\n' "$SUP" | grep '松判据')
  if [ -n "$hit" ]; then
    printf '   %s\n' "$hit"
    echo "   PASS: 那一句在"
  else
    echo "   FAIL: 补卡那一节没有「松判据」——后门那一句被删了"
    fail=1
  fi
fi

echo
echo "== E 冻结那一条没被松：必须恰好一处「许可面定在结案，结案之前退回闸一才改得动，改完要重提」 =="
echo "   （绊线，不是待补项。先红后绿那一次它就该是绿的；红了说明脚本写反了）"
d=$(grep -cF '许可面定在结案，结案之前退回闸一才改得动，改完要重提' "$W")
echo "   新锚点出现 $d 处"
if [ "$d" -eq 1 ]; then
  grep -n '许可面定在结案，结案之前退回闸一才改得动，改完要重提' "$W" | sed 's/^/   /'
  echo "   PASS: 恰好一处"
else
  if [ "$d" -eq 0 ]; then
    echo "   FAIL: 一处都没有——补卡被读回成往老卡上追加了，或者新规矩那条承重句被删了"
  else
    echo "   FAIL: 应为 1 处——多一处说明有人复述了承重句"
  fi
  fail=1
fi

echo
echo "== F 理由没被当成修辞删掉：必须出现「一事一结」 =="
echo "   （补卡这一节的承重墙。理由一没，规矩就只剩手续）"
hit=$(grep -n '一事一结' "$W")
if [ -n "$hit" ]; then
  printf '   %s\n' "$hit"
  echo "   PASS: 理由在"
else
  echo "   FAIL: 「一事一结」不见了——补卡只剩手续，下一个人会当成税删掉"
  fail=1
fi

echo
echo "== G 跟稿那条时点没被删：必须出现「跟一稿」 =="
echo "   （卡每改一稿，上半页跟一稿。它一没，审卡又会读到一份对不上的运行态）"
hit=$(grep -n '跟一稿' "$W")
if [ -n "$hit" ]; then
  printf '   %s\n' "$hit"
  echo "   PASS: 时点在"
else
  echo "   FAIL: 「跟一稿」不见了——② 那一段又没写时点了"
  fail=1
fi

echo
if [ "$fail" -eq 0 ]; then
  echo "ALL PASS"
else
  echo "FAILED"
fi
exit "$fail"
