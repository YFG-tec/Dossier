#!/usr/bin/env bash
# 已办区验收：勾完不删，移进 todo.md 末尾的「已办」，每行点名一份 cmd/。
# 零权威，只作证，不算「通过」。用法：bash docs_meta/tests/check-done.sh
#
# 口径（脚本和文档必须同一套）：
#
#   A 一一对应 —— 每份 cmd/PROMPT_xx.md 在 todo.md **整页恰好出现一次**；
#     每条已办恰好点名一份存在的 cmd。
#     **2026-09-08 闸二人裁：「还是一一对应」，取严口径——散文里多提一次也算超额。**
#     所以一份 cmd 在那一页只有一个落点，就是它自己那一行；要说的话写进那两行里。
#     （红后我曾把口径改成「只数条目行」，人已裁回严的。改口径 = 发授权 = 人的那一爪。）
#     **在办的那一刀点名自己的卡是合法的**，它的行还在待办区——对应的是「条目」，不是「已办条目」。
#     **卡号 2026-09-09 改成三位定长流水 PROMPT_000**（人裁），从此和 todo 编号脱钩：
#     编号是可重排的管理视图，卡号是永不改名的身份锚。改过两次，这是最后一次。
#     **定长补零顺手把前缀 bug 除了根**：PROMPT_1.1 曾是 PROMPT_1.10 的前缀，
#     而 PROMPT_007 永远不是 PROMPT_070 的前缀。数出现次数仍带 `.md` 后缀、用 -F，
#     那是第二道保险，不再是唯一那道。
#     **正则写 [0-9]{3,} 而不是 {3}——三位是下限不是上限。** 第 1000 张卡自然写成
#     PROMPT_1000，位宽只增不减，不用重新补零。要是写死 {3}，那天它会把 PROMPT_1000
#     截成 PROMPT_100 —— **凭空造出一个真实存在的卡号，而且不会有任何东西变红。**
#     **原来这里留了个退卡白名单 DROPPED，2026-09-09 连同注释一起删了**——不是放宽，是**死码**。
#     它当初是为「退卡的一刀有 cmd 却永远没有已办行」预留的口子；那天人裁「只有尘埃落定的卡
#     才永久记录」，**退掉的卡当场删**，孤儿 cmd 从此不会产生，白名单永远匹配不上。
#     留着白名单反而危险：它是一条现成的「点名放过某张卡」的通道（paradigm.md §5：
#     例外清单下一个人只会往上加名字，不会往下删）。
#     **同一面墙上的另一个洞也是那天堵的**：免卡的活（`examples/`）根本不进 TODO，
#     不需要已办落点，所以也不需要口子。两个洞都不再靠白名单挡。
#
#   B 不变胖 —— 已办行只许是「原措辞 + 一个 cmd 指针 + 日期」。
#     已办区比待办区更危险：待办会被勾掉，已办永远在。
#
#   C 同口径 —— 旧口径「勾完删行」/「勾完就删」不许再作为**现行规矩**出现。
#     **放行条件：同一行还出现「旧」/「以前」/「不再」/「改成」。**
#     不是禁这四个字，是禁它当规矩讲——「以前是勾完就删」是在讲来历，
#     而**规矩不带理由就会被下一个人当税删掉**（§10 自己写的），所以来历必须讲得了。
#     形状抄自 check-cmd.sh 的 A 条：同一行出现放行词才放过。
#     **能机检的是词的共现，不是意思**——这就是共现能做到的上限。
#     **这里不套上一刀的「用 / 提」约定，扫原文。** 那条约定是为「标记发不发授权」立的：
#     代码块里的【定】不发授权，所以要剥。C 问的是另一件事——旧口径还在不在，
#     而 workflow.md:131 那张状态表**本身就在陈述口径**，它在围栏里也照样算数。
#     剥了就漏。**判据要跟着问题走，不跟着上一条判据走。**
#     cmd/ 是只增不删的历史，一律不扫。
#     **2026-09-11 扫描名单去掉了 `paradigm.md`**（`cmd/PROMPT_013.md` 第 12 件）：
#     那一刀把 `design/` 从红绿判定里剥出去，不在思路层的文件上做机械断言。
#     人当天落槌「字面退役」——减扫描目标是放宽，不由测试这只手自己做。
#     **代价照写**：`paradigm.md` 里要是把旧口径当现行规矩写回来，不会有东西红。
#     `workflow.md` / `directory.md` / `todo.md` 三项照旧，那三处才是口径的正身。
#
# 这三条查的是**指针对不对得上**，查不了「这一刀到底干成了没有」——那是人的判断。
cd "$(dirname "$0")/../.."
fail=0
TODO=docs_meta/docs/todo.md
CMDDIR=docs_meta/docs/cmd

# 条目 = 「- [ ]」/「- [x]」开头的行 + 其后的缩进续行。输出：行号 <TAB> 占几行 <TAB> 全文
# 参数：$1 起始行号（0 = 全文），$2 勾选态正则
#
# **围栏内一律跳过**——已办区自己写着格式样例，样例长得和条目一模一样，
# 检查器不能把自己的格式说明当数据读。
# **散文段落也要跳过**：顶格的非条目行终结当前条目，否则说明文字会被并进上一条。
rows() {
  awk -v s="$1" -v pat="$2" '
    NR>s {
      if ($0 ~ /^```/) { b=!b; next }
      if (b) next
      if ($0 ~ pat) { if (buf!="") print n "\t" cnt "\t" buf; n=NR; cnt=1; buf=$0 }
      else if ($0 ~ /^[[:space:]]+[^[:space:]]/ && buf!="") { cnt++; buf=buf " " $0 }
      else if ($0 !~ /^[[:space:]]*$/) { if (buf!="") { print n "\t" cnt "\t" buf; buf="" } }
    }
    END { if (buf!="") print n "\t" cnt "\t" buf }' "$TODO"
}
# 反斜杠写两道：shell 吃一道，awk 的动态正则吃一道。
entries() { rows "$start" '^- \\[x\\]'; }      # 已办区的条目

echo "== A 一一对应：每份 cmd 在 todo.md 整页恰好出现一次，每条已办恰好点名一份 cmd =="

start=$(grep -n $'^## 已办' "$TODO" | head -1 | cut -d: -f1)
if [ -z "$start" ]; then
  echo "   FAIL: todo.md 里没有「## 已办」这一节——勾完的行无处可去"
  fail=1
  start=$(wc -l < "$TODO")
fi

# 方向一：每个卡号在 todo.md 整页恰好出现一次（严口径，人裁）。
# 数的是**出现次数**不是行数——同一行写两遍也是两次。
for f in "$CMDDIR"/PROMPT_*.md; do
  name=$(basename "$f" .md)
  n=$(grep -oF "$name.md" "$TODO" | wc -l)   # 带 .md 后缀：定长补零之后这已是第二道保险
  if [ "$n" -eq 1 ]; then
    echo "   $name  OK"
  else
    echo "   $name  FAIL: 在 todo.md 整页出现 $n 次，应为 1"
    fail=1
  fi
done

# 方向二：页上提到的每个卡号都得真有文件
for name in $(grep -oE 'PROMPT_[0-9]{3,}' "$TODO" | sort -u); do
  [ -f "$CMDDIR/$name.md" ] || { echo "   FAIL: todo.md 点名 $name，但 $CMDDIR/$name.md 不存在"; fail=1; }
done

# 方向三：已办区每一条恰好点名一份
nd=0
while IFS=$'\t' read -r no cnt txt; do
  [ -z "$no" ] && continue
  nd=$((nd+1))
  k=$(printf '%s' "$txt" | grep -oE 'PROMPT_[0-9]{3,}' | sort -u | wc -l)
  if [ "$k" -ne 1 ]; then
    echo "   第 $no 行  FAIL: 这条已办点名了 $k 份 cmd，应为 1"
    fail=1
  fi
done < <(entries)
echo "   已办区共 $nd 条"
[ "$nd" -eq 0 ] && { echo "   FAIL: 已办区一条都没有——历史没搬过来"; fail=1; }

echo
echo "== B 不变胖：已办行只许是「原措辞 + 一个 cmd 指针 + 日期」 =="
echo "   （已办区比待办区更危险：待办会被勾掉，已办永远在）"
while IFS=$'\t' read -r no cnt txt; do
  [ -z "$no" ] && continue
  if [ "$cnt" -gt 2 ]; then
    echo "   第 $no 行  FAIL: 这条占 $cnt 行，上限 2"
    fail=1
  fi
  if ! printf '%s' "$txt" | grep -qE '20[0-9][0-9]-[0-9][0-9]-[0-9][0-9]'; then
    echo "   第 $no 行  FAIL: 没有结案日期"
    fail=1
  fi
  for bad in $'拍板' $'验收' $'完成标准'; do
    if printf '%s' "$txt" | grep -q "$bad"; then
      echo "   第 $no 行  FAIL: 出现「$bad」——细节往 design / cmd 走，不往这里塞"
      fail=1
    fi
  done
done < <(entries)
[ "$fail" -eq 0 ] && echo "   PASS: 每条都只有措辞、指针、日期"

echo
echo "== C 同口径：旧口径不许再作为现行规矩出现 =="
echo "   （扫原文，不剥围栏——状态表本身就在陈述口径；cmd/ 是历史，不扫）"
echo "   （放行条件：同一行还出现「旧」/「以前」/「不再」/「改成」——那是在讲来历，不是在立规矩）"
for f in docs_meta/src/workflow.md docs_meta/src/directory.md "$TODO"; do
  hit=$(grep -n $'勾完删行\|勾完就删' "$f" | grep -v $'旧\|以前\|不再\|改成')
  if [ -n "$hit" ]; then
    echo "   $f"
    printf '   %s\n' "$hit"
    echo "   FAIL: 旧口径还在——寿命改了，这句没改就是静默降档"
    fail=1
  else
    echo "   $f  OK"
  fi
done

echo
if [ "$fail" -eq 0 ]; then echo "ALL PASS"; else echo "FAILED"; fi
exit $fail
