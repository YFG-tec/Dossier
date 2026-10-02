#!/usr/bin/env bash
# 第二份记录验收：第 n 份一律写成链接，不抄。零权威，只作证，不算「通过」。
# 用法：bash docs_meta/tests/check-link.sh
#
# **现在五段**：A / B / C 查链接，**D 查闸一红印**（2026-09-09 由 PROMPT_008 加），
#   **E 查横线以下没堆旧刀**（2026-09-23 由 PROMPT_038 加）。
# **名字对不上，故意不改**——它叫 check-link，现在 D、E 两段查的都不是链接。
# 名字是历史（同 check-mark.sh 那一裁），改名是以后搬 test/ 时的事。
#
# 口径（脚本和文档必须同一套）：
#
#   A 没有第二份 —— SESSION.md 里不许出现卡片的字段名
#     （「本刀是 TODO 哪一行」/「交什么」/「不交什么」/「禁令」）。出现了就是又抄了一份卡。
#     **不设放行词。** check-cmd.sh A 和 check-done.sh C 都留了「同一行还出现某某就放过」，
#     这一条**故意不留**：留了就等于说「指路时提一句字段名可以」，
#     而「提一句」和「顺手抄一段」之间没有机器分得清的界。
#     代价照写：SESSION.md 想指路时不能写「交什么见卡片」，只能写「细则见卡片」。
#     **这是紧口径。放宽 = 挪门槛 = 人的那一爪**，实现和测试都不许自己改。
#
#   B 有链接 —— SESSION.md 必须出现 cmd/PROMPT_NNN.md 指针，**恰好一处**。
#     卡号 2026-09-09 与编号脱钩，改成三位流水 PROMPT_NNN，正则是 [0-9]{3,}；
#     `{3,}` 是下限不是定长——过千长成四位，写死 {3} 会把 PROMPT_1000 截成 PROMPT_100，
#     凭空指向另一张真卡而不红。后缀 `.md` 必须带上。
#     恰好一处，不是至少一处：多一处就多一个要同步的落点，
#     和「一份 cmd 在 todo.md 整页恰好一次」（check-done.sh A）同一个形状。
#
#   C 链接不悬空 —— B 数出来的那份 cmd/ 必须真的存在。
#     2026-09-09 补。**这是收紧，不是放宽**：原来语法对就算过，现在还要文件在。
#     收紧是测试那只手的本职（paradigm.md §3 第 4 条：松判据才是人的那一爪），
#     所以这一条不需要另发一次授权。补它的由头是同一天定的退卡规矩——
#     **退掉的卡要删**，删完 SESSION 那个指针就悬空了，而 B 只看语法，一个字都不会红。
#
#     **已知缺口，本刀不裁，别当它已经答了：** 退卡之后到下一张卡发出之前那段空窗，
#     SESSION 该怎么写，现在没有合法写法——照实写「已退卡、暂无卡」→ 指针 0 处 → B 红；
#     把已删卡片的旧指针留着不动 → B 绿、C 红。**A/B/C 三条合起来目前奖励不了诚实的那一种。**
#     实践上这段空窗极短（退卡必然回 ② 重写卡，新卡一发 SESSION 就被整篇覆盖），
#     所以先记着，不为它开口子——**开口子就是放宽，那是人的那一爪。**
#
#   D 闸一红印 —— 横线以上**「同一行既有固定词『闸一红印』、又有日期」的行，至少一处**。
#     2026-09-13 从「恰好一处」改成「至少一处」，理由：冻结点后移后退回闸一会重提，红印会重落。
#     检查存在性，不检查数量。版次形状（版次连号、最大版次唯一）由 check-gate.sh 守。
#     2026-09-09 由 PROMPT_008 加。**这是收紧，不是放宽**：原来「过闸了」只活在聊天里，
#     现在必须在盘上留一颗能 grep 的印。收紧是测试那只手的本职（同 C 那条理由），不另发授权。
#
#     **判据的形状是「词 + 日期共现」，不是词频。** SESSION.md 那一节的标题本身就含这个词，
#     按词频数的话，**印一落就是两处，永远红**——和 A 段撞「禁令」同一个形状。
#     共现是形状，**不是放行词**（paradigm.md §6：能机检的是词的共现，不是意思）。
#     标题只含词、不带日期，所以数不到它；印文那一行两样都有，所以数得到。
#
#     **不设放行词**，同 A 那条理由：留了放行词，「文里提一句红印」和「真落一颗红印」
#     之间就没有机器分得清的界。
#
#     **红是正常态，不是坏了：** ② 写卡阶段还没过闸，这一条必红；
#     人说「按卡片做」、印落下，才转绿。**此后每一刀都会先红后绿。**
#
#     **它查不了什么，照写不吹：** 查得了印在不在、那一行带没带日期，
#     **查不了那句话是不是真有人说过**。落印的手往往就是等着开工的那只手，形式上是自证——
#     唯一的防线是「逐字抄原话」，那是纪律，不是判据。
#
#   E 横线以下没有旧刀 —— 横线以上指着当前卡时，横线以下不许出现别刀的标题行。
#     2026-09-23 由 PROMPT_038 加。**这是收紧，不是放宽**（同 C / D 那两条理由），不另发授权。
#     本刀行号从横线以上「点的行」那格现算（第一个 X.Y 形 token，可带字母尾），
#     本刀卡号从横线以上唯一的 cmd/PROMPT_ 指针现算（取 NNN，比数字部分）。
#     **两者有一个现算不出来 → E 段 FAIL**（宁可响，不许静默绿——check-trace A 段同款哲学）。
#     横线以下凡 # 开头的行，含行号形（数字.数字，可带字母尾）或卡号形（PROMPT_数字）token
#     且 ≠ 本刀的，红，点名行号和内容。不含编号的标题放过。
#     **正文行不扫**——正文引别刀是常态（`4.10` 审卡页引过 `4.9`、`3.3`），扫了全是假红。
#     代价照写：标题里引别刀编号也红（哪怕正当引用），这逼出干净的标题，是特性；
#     反过来把旧刀内容塞进无编号标题或正文，E 段看不见——两头都是「机检形状不检意思」的标准代价。
#
#   **两条都扫原文，不剥围栏。** 上一刀那条「裸的是授权、围栏里的是提及」是为标记立的；
#   这里问的是另一件事——**有没有第二份内容**，而围栏里的内容也是内容。
#   判据要跟着问题走，不跟着上一条判据走。
#
# 三条拦得住「又抄了一份」和「指了个不存在的」，**仍拦不住「指错了刀」**——
# 指向另一张真卡照样全绿。照写，不吹（paradigm.md §6：能机检的是词的共现，不是意思）。
#   **射程：只扫横线以上**（2026-09-09 补，跟 `本页两截` 那一裁）。
#     人 2026-09-09 裁：`SESSION.md` 横线以上由写卡那只手起草，横线以下只追加审阅，形同审稿。
#     **审阅要指出「第 8 条写错了」，就必须点那一条的名字**——那不是抄了第二份卡，
#     是审稿意见的正常形态。A / B 原来扫全页，于是把审稿意见判成了第二份卡。
#     所以射程收到第一条 `^---$` 之前。**断言本身一个字没松**：
#     写卡那只手仍然不许在自己那半页复述字段、仍然只许留一个指针。
#
#     **开的口子照写，不粉饰：** 有人把整张卡抄到横线以下，A 不会红。
#     赌的是那半页只有人自己写、且它是审稿而不是许可面（横线以下明写「不改卡」）。
#     **要堵就得另立一条查「横线以下有没有整段抄」，本刀没做。**
#
# SESSION 路径用的根目录开关：环境变量 LINK_ROOT，默认仓库根（不设时路径不前缀，行为一字不变）。
#   形状照 check-lock.sh 的 LOCK_ROOT。设成假树根时，A–E 五段都读那一棵，探针走这一路，不写 live SESSION。
#   **run.sh 走默认那一路，不带参数、不设这个变量。**
cd "$(dirname "$0")/../.."
fail=0
ROOT="${LINK_ROOT:-}"
ROOT="${ROOT%/}"
S="${ROOT:+$ROOT/}docs_meta/docs/SESSION.md"
FULL="$S"   # 原文整页，E 段扫横线以下要用它（S 稍后被换成「横线以上」那份）

[ -f "$S" ] || { echo "FAIL: $S 不存在"; exit 1; }

# 横线以上 = 写卡那只手的那半页。没有横线就是全页（本页两截之前的老格式）。
TOP=$(mktemp)
trap 'rm -f "$TOP"' EXIT
if grep -qn '^---$' "$S"; then
  awk '/^---$/{exit} {print}' "$S" > "$TOP"
  echo "（射程：横线以上 $(wc -l < "$TOP") 行；横线以下是审阅记录，不扫——见脚本头）"
else
  cp "$S" "$TOP"
  echo "（射程：全页，本页没有横线）"
fi
S="$TOP"

echo "== A 没有第二份：SESSION.md 里不许出现卡片的字段名 =="
echo "   （不设放行词——「提一句」和「抄一段」之间没有机器分得清的界）"
a=0
for f in $'本刀是 TODO 哪一行' $'交什么' $'不交什么' $'禁令'; do
  hit=$(grep -n "$f" "$S")
  if [ -n "$hit" ]; then
    echo "   「$f」"
    printf '   %s\n' "$hit"
    a=1
  else
    echo "   「$f」  OK: 没出现"
  fi
done
if [ "$a" -eq 0 ]; then
  echo "   PASS: SESSION 里没有卡片的字段"
else
  echo "   FAIL: 上面这些字段是卡片的；SESSION 复述了它们就是第二份卡"
  fail=1
fi

echo
echo "== B 有链接：SESSION.md 必须有 cmd/PROMPT_NNN.md 指针，恰好一处 =="
n=$(grep -oE 'cmd/PROMPT_[0-9]{3,}\.md' "$S" | wc -l)
echo "   指针出现 $n 次"
grep -nE 'cmd/PROMPT_[0-9]{3,}\.md' "$S" | sed 's/^/   /'
if [ "$n" -eq 1 ]; then
  echo "   PASS: 恰好一处"
else
  echo "   FAIL: 应为 1 次——0 次是没链接，多次是多了要同步的落点"
  fail=1
fi

echo
echo "== C 链接不悬空：被指的那份 cmd/ 必须存在 =="
echo "   （退卡要删卡；删完 B 仍然绿，因为 B 只看语法）"
c=0
ptrs=$(grep -oE 'cmd/PROMPT_[0-9]{3,}\.md' "$S" | sort -u)
if [ -z "$ptrs" ]; then
  echo "   SKIP: B 没数到指针，这一条无从查起（红已经记在 B）"
else
  for p in $ptrs; do
    if [ -f "${ROOT:+$ROOT/}docs_meta/docs/$p" ]; then
      echo "   docs_meta/docs/$p  OK: 在"
    else
      echo "   docs_meta/docs/$p  FAIL: 不存在——指针悬空"
      c=1
    fi
  done
  if [ "$c" -eq 0 ]; then
    echo "   PASS: 指到的卡都在"
  else
    echo "   FAIL: SESSION 指着一份不存在的卡"
    fail=1
  fi
fi

echo
echo "== D 闸一红印：横线以上「同一行既有『闸一红印』又有日期」的行，至少一处 =="
echo "   （数的是共现，不是词频——标题只含词、不带日期，数不到它）"
dhits=$(grep -n '闸一红印' "$S" | grep -E '20[0-9][0-9]-[0-9][0-9]-[0-9][0-9]')
if [ -z "$dhits" ]; then d=0; else d=$(printf '%s\n' "$dhits" | wc -l); fi
echo "   带日期的红印行 $d 处"
[ -n "$dhits" ] && printf '   %s\n' "$dhits"
if [ "$d" -ge 1 ]; then
  echo "   PASS: 至少一处"
elif [ "$d" -eq 0 ]; then
  echo "   FAIL: 一处都没有——闸一还没过，或者过了没落印"
  echo "         没有红印，实现不许落第一笔（写卡阶段红是正常的）"
  fail=1
fi

echo
echo "== E 横线以下没有旧刀：指着当前卡时，横线以下不许出现别刀的标题行 =="
echo "   （正文行不扫——正文引别刀是常态，扫了全是假红；见脚本头）"
# 本刀行号：横线以上「点的行」那格第一个 X.Y 形 token（可带字母尾）。
ROW=$(grep -F '点的行' "$S" | grep -oE '[0-9]+\.[0-9]+[a-z]*' | head -n1)
# 本刀卡号：横线以上唯一的 cmd/PROMPT_NNN.md 指针（NNN 现算，比数字部分）。
CARD_LIST=$(grep -oE 'cmd/PROMPT_[0-9]{3,}\.md' "$S" | sort -u)
NCARD=$(printf '%s\n' "$CARD_LIST" | grep -c .)
if [ -z "$ROW" ] || [ "$NCARD" -ne 1 ]; then
  echo "   FAIL: 本刀口径现算不出来，E 段宁可响不许静默绿"
  if [ -z "$ROW" ]; then echo "         「点的行」那格里没读到 X.Y 形行号"; fi
  if [ "$NCARD" -ne 1 ]; then echo "         横线以上 cmd/PROMPT_ 指针不唯一（读到 $NCARD 个不同指针）"; fi
  fail=1
else
  CARD=$(printf '%s' "$CARD_LIST" | sed 's/.*PROMPT_//; s/\.md$//')
  echo "   本刀行号=$ROW 本刀卡号=$CARD"
  sep=$(grep -n '^---$' "$FULL" | head -n1 | cut -d: -f1)
  if [ -z "$sep" ]; then
    echo "   （本页没有横线，横线以下无内容可扫）"
    echo "   PASS: 横线以下没有带别刀编号的标题"
  else
    e_hit=0
    nr=0
    while IFS= read -r line || [ -n "$line" ]; do
      nr=$((nr + 1))
      if [ "$nr" -le "$sep" ]; then continue; fi
      case "$line" in
        \#*)
          bad=""
          for t in $(printf '%s\n' "$line" | grep -oE '[0-9]+\.[0-9]+[a-z]*'); do
            if [ "$t" != "$ROW" ]; then bad="$bad $t"; fi
          done
          for t in $(printf '%s\n' "$line" | grep -oE 'PROMPT_[0-9]+'); do
            if [ "${t#PROMPT_}" != "$CARD" ]; then bad="$bad $t"; fi
          done
          if [ -n "$bad" ]; then
            e_hit=1
            printf '   FAIL: 第 %s 行是别刀的标题，含编号:%s\n' "$nr" "$bad"
            printf '         标题：%s\n' "$line"
          fi
          ;;
      esac
    done < "$FULL"
    if [ "$e_hit" -eq 0 ]; then
      echo "   PASS: 横线以下没有带别刀编号的标题"
    else
      fail=1
    fi
  fi
fi

echo
if [ "$fail" -eq 0 ]; then echo "ALL PASS"; else echo "FAILED"; fi
exit $fail
