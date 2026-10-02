#!/usr/bin/env bash
# 审查那只手的指纹检查。零权威，只作证，不算「通过」。
# 用法：bash docs_meta/tests/check-trace.sh            空跑：自检取法。run.sh 走这一路
#       bash docs_meta/tests/check-trace.sh take       印一份指纹到 stdout
#       bash docs_meta/tests/check-trace.sh diff A B   两份比，不一致退出码 1
#
# 谁加的：2026-09-12 由 cmd/PROMPT_016.md 新增，实现席这只手写的。
# A 段空输出判据 2026-09-25 改（6.25）：退码非零=取失败必红；空+退码0=干净树合法。B/C/D 一字未动。
# **这是收紧，不是放宽**，所以不另发一次授权（paradigm.md §3 第 4 条：松判据才是人的那一爪）。
# 同 check-lock.sh 整本、check-word.sh 整本那条理由。
#
# 为什么要有第十一本：原有十本查的都是「盘上写着什么」，一本都不查「这一趟改了什么」。
#   重档下领班要往外派子代理（.claude/agents/review.md），那只手写着零写权限，
#   但零写只活在正文里——工具面给了它 Bash，Bash 改得动盘。
#   具体后果：审查那只手在自己审的那一刀里顺手改了产物，十本全绿，没有东西会红。
#   本刀补的就是这一格：派发前后各取一份指纹，比一次。
#
# 钉的是哪几裁：
#   **射程是整个工作树**（人 2026-09-12 原话：射程收窄那一支「我想错了，按照你的来就行」）。
#     收窄到「src/ 和生成的规则 / 角色文件」会漏掉 .tmp/ 和 docs_meta/tests/，
#     而那两处恰好是审查那只手最可能落笔的地方——
#     行上明写它连 .tmp/ 都不许写，review.md 自己写着它的 Bash 就在 tests/ 下跑。
#   **2026-09-22 松了一格：.venv/ 排出射程**（人松判据原话逐字：
#     「能出图就行，这个放宽，坚决不审 .venv 要不然啥都别干了」；
#     同日点名钦差办理，原话逐字：「你派一个subagent，算是钦差，去把这个.venv 的指纹验收给处理了」；
#     立案 todo.md 4.9）。上面那行「射程是整个工作树」从这一裁起读成「整个工作树减 .venv/」。
#     为什么松：.venv/ 下 4278 份 PIL/numpy 文件全在 --ignored -uall 的射程里，
#     逐份起一次 git hash-object，一次指纹拖到十几分钟，拖垮整盘——慢在逐份哈希的进程开销，
#     status 自己扫树不足一秒。
#     落地就一处：status 的 pathspec 加 -- ':(exclude).venv'，取法其余一个字不动。
#     **松的只有这一格**：.tmp/ 的 --ignored、-uall 两个保证（B、C 段自检）一律不动，
#     射程其余部分不动；排除锚在根，嵌套在别处的 .venv/ 不在豁免之内。
#     这道裁明付的代价，写在下面「查不到什么」第一条。
#   **两个开关都要**（本刀实测）：缺 --ignored，.tmp/ 整层看不见；
#     缺 -uall，已经在报的那个 ignored 目录塌成一行，里面改什么都不动指纹。
#   **内容哈希比行上写的宽**（收紧，写明）：行上写的是「未跟踪文件的哈希」，
#     本刀对状态行报出来的每一份普通文件都算哈希，跟踪的那几份也算。
#     理由：一份被改过的跟踪文件前后都是「 M」，只看状态行分不出它被改了两遍。
#   **派是收口那一步的对象，不是断言格**（人 2026-09-12 原话：
#     「先是收尾对象，如果检测出红，会上报，视严重程度进行补充或退卡，按这个来就行，
#     后面全自动化之后，就会变成断言对象」）。所以本脚本只答一致不一致，
#     轻重由人裁，领班不许自己消化那个红。
#
#   **取出来的那一份不许落在射程里。** 本刀实测撞到的，写进口径省得下一只手再撞：
#     射程是整个工作树含 ignored 那一层，所以 .tmp/ 下的指纹文件、日志，自己也在射程里。
#     take 重定向到 .tmp/xxx.txt 的那一瞬间壳先把它截空，那一份就把「自己是空的」记了进去；
#     隔一会儿再取第二份，第一份已经写满，哈希对不上——**前后两份必然不一致，而且全是自指**。
#     那种红是假红，红的是领班自己的笔，不是被测的那只手，
#     会把「派发前后比一次」这件事整个废掉（卡 PROMPT_016 第 4 件写死了这一点）。
#     **正确取法**：两份都先落到工作树外面（/tmp 之类），或者先进变量，
#     两次都取完之后再把它们搬进 .tmp/。搬的动作发生在第二次取之后，污染不到任何一次。
#
#   **同一个坑在 run.sh 那一层再咬一次，一起写明。** 空跑的 D 格要求「清掉探针，指纹回到 A」，
#     所以从 A 取到 D 取这段时间里，射程内任何东西变了都会红。
#     `bash docs_meta/tests/run.sh > .tmp/xxx.log` 就会红——那份日志一边长一边被算进指纹，
#     红的是重定向，不是探针没清干净。本刀实测过：日志落 .tmp/ 里 rc=1，落工作树外 rc=0，
#     两次盘上别的东西一个字没差。
#     **run.sh 直接印到终端不受影响**，要存日志就存到工作树外面。
#     这一格没做成「自动忽略自己的日志」，因为那是放宽射程，**放宽是人的一爪**；
#     宁可留一条会咬人的真射程，也不要一条自己给自己开洞的假射程。
#
# 口径（脚本和文档必须同一套）：
#
#   指纹怎么算，写死：
#     git -c core.quotepath=false status --porcelain -uall --ignored -- ':(exclude).venv'   状态行，排序
#     （那段排除是人 2026-09-22 那道裁加的，来历见上面「钉的是哪几裁」）
#     每一条报出来的路径，只要是普通文件，再算一次内容哈希
#   core.quotepath=false 是为了非 ASCII 路径不被转义成 \xxx。
#   本机 locale 的坑记在 PROMPT_015，同一类。
#
#   空跑那一路查四格，四格都是自检取法，不是自检审查那只手：
#
#   A 取得到 —— 取一次，退出码 0，输出非空。
#     取不到就红：没有 git、命令非零、目录读不到，都算红。
#     **不许静默绿。** 取指纹这一步自己失败了算红，不算「这一趟没改」。
#
#   B --ignored 没掉 —— 在 .tmp/ 下造一个新目录带一份文件，再取，必须和 A 不同。
#     红了指：--ignored 掉了，.tmp/ 整层不在射程。
#
#   C -uall 没掉 —— 往同一个目录里再加一份，再取，必须和 B 不同。
#     红了指：-uall 掉了，目录塌着，里面改什么都不动指纹。
#     **这一格是本刀实测出来的，坑比想的窄**：塌不塌要看那个目录在不在报。
#     往全新的 .tmp/<目录>/ 放探针，不加 -uall 也看得见（多出那个目录一行）；
#     往早就在报、已经塌着的目录里放，不加 -uall 一行都不多。
#     所以探针要造两次，只造一次的话这一格永远绿。
#
#   D 可逆 —— 清掉探针目录，再取，必须和 A 逐字相同。
#     红了指：探针没清干净，或者指纹不可逆。
#
#   **探针目录名现算，不写死**，带一次 $$，免得两次并跑互相撞。
#   **探针有 trap 清场**：脚本半路死掉不许把探针留在 .tmp/ 里。
#   留下了，后面每一次取指纹都带着它，而且不会有东西红。
#
# **它查不到什么，照写不吹：**
#
#   查不到 **.venv/ 里改了什么**。人 2026-09-22 那道裁把它整层排出射程（见上）。
#     有手往 .venv/ 里落笔，这一本不红——那是那道裁明付的代价，不是漏。
#
#   查不到**是哪只手改的**。指纹只答盘变没变。
#     重档下派出去的是子代理，但指纹分不出是它写的还是领班顺手写的。
#
#   **是事后，不是事前**。不阻止那一次写，只保证那一次写藏不住。
#     事前硬拦在本 harness 的工具面拿不到，三条路各自的代价写在 PROMPT_014 末节。
#
#   查不到**内容对不对**。口径是「变没变」，不是「变得对不对」。
#
#   查不到 2.6a、2.6b 那两趟有没有越界。**从装上这一刀起算**，追不回去。
#
#   空跑那一路查不到任何一次真实的派发。它只查取法本身——
#     **空跑永远断言不了「这一趟有没有改盘」**，因为空跑的时候没有「这一趟」。
#
#   查不到 .gitignore 改了之后指纹为什么会跳。ignore 集合变了指纹就变，那不是越界。
#
#   **永远断言不了「派过了」。** 它只答盘变没变，答不了中间发生过什么。
#     要让「派没派」变成机械断言，得另找一个落盘的物证，那是另一本，不是把这一本喂胖。
#
#   空跑那一路是恒不恒绿，取决于 .tmp/ 写得进去。写不进去会红在 A 或 B 格，
#     红的理由和「越界」无关，**不许读成有手越界了**。
cd "$(dirname "$0")/../.."

# ---- 取一份指纹 ----
take() {
  git -c core.quotepath=false status --porcelain -uall --ignored -- ':(exclude).venv' | LC_ALL=C sort | while IFS= read -r line; do
    path=${line#???}
    if [ -f "$path" ]; then
      h=$(git hash-object "$path" 2>/dev/null || echo "HASHFAIL")
      printf '%s  %s\n' "$line" "$h"
    else
      printf '%s\n' "$line"
    fi
  done
}

mode=${1:-selftest}

case "$mode" in
  take)
    out=$(take) || { echo "取不到指纹" >&2; exit 1; }
    [ -n "$out" ] || { echo "指纹为空——取不到，不算「没改」" >&2; exit 1; }
    printf '%s\n' "$out"
    exit 0
    ;;
  diff)
    a=$2; b=$3
    [ -f "$a" ] && [ -f "$b" ] || { echo "diff 要两份都在：$a $b" >&2; exit 1; }
    if command diff -u "$a" "$b" >/dev/null; then
      echo "指纹一致：$a == $b"
      exit 0
    else
      echo "指纹不一致，这一趟改了盘："
      command diff -u "$a" "$b" | sed 's/^/   /'
      exit 1
    fi
    ;;
  selftest)
    ;;
  *)
    echo "不认得的用法：$mode" >&2
    exit 1
    ;;
esac

# ---- 空跑：自检取法 ----
fail=0
probe=".tmp/trace-probe-$$"

cleanup() { rm -rf "$probe"; }
trap cleanup EXIT INT TERM

echo "（射程：整个工作树减 .venv/，含 ignored 那一层——.venv/ 排出是人 2026-09-22 那道裁，todo.md 4.9，见脚本头。空跑只自检取法，不自检任何一次真实派发——见脚本头）"
echo

echo "== A 取得到：取一次，退出码 0（6.25 改：空输出=干净树，不是取失败）=="
echo "   （取不到就红，不许静默绿——退码非零才算取失败；fresh clone 上 .tmp/ 是空的，"
echo "     status 零行、指纹合法为空——041 那族「尺子量错对象」的第三标本，本刀拆掉）"
fpA=$(take)
rcA=$?
if [ "$rcA" -ne 0 ]; then
  echo "   FAIL: 取指纹退出码 $rcA"
  fail=1
elif [ -z "$fpA" ]; then
  echo "   OK   干净树：status 零行，指纹合法为空（B/C/D 照跑：造探针后非空、清回后仍等 A）"
  echo "   PASS: 取得到"
else
  echo "   OK   取到 $(printf '%s\n' "$fpA" | wc -l) 行"
  echo "   PASS: 取得到"
fi

echo
echo "== B --ignored 没掉：.tmp/ 下造一个新目录带一份文件，指纹必须变 =="
echo "   （红了指 --ignored 掉了，.tmp/ 整层不在射程）"
mkdir -p "$probe"
echo "probe one" > "$probe/one.txt"
fpB=$(take)
if [ "$fpA" != "$fpB" ]; then
  echo "   OK   指纹变了"
  echo "   PASS: .tmp/ 在射程里"
else
  echo "   FAIL: 造了 $probe/one.txt，指纹一个字没变——.tmp/ 不在射程"
  fail=1
fi

echo
echo "== C -uall 没掉：往同一个目录里再加一份，指纹必须再变 =="
echo "   （红了指 -uall 掉了，目录塌成一行，里面改什么都不动指纹）"
echo "probe two" > "$probe/two.txt"
fpC=$(take)
if [ "$fpB" != "$fpC" ]; then
  echo "   OK   指纹又变了"
  echo "   PASS: 目录里面看得见"
else
  echo "   FAIL: 往 $probe/ 里加了第二份，指纹一个字没变——目录塌着"
  fail=1
fi

echo
echo "== D 可逆：清掉探针目录，指纹必须和 A 逐字相同 =="
echo "   （红了指探针没清干净，或者指纹不可逆）"
cleanup
fpD=$(take)
if [ "$fpA" = "$fpD" ]; then
  echo "   OK   回到 A"
  echo "   PASS: 可逆"
else
  echo "   FAIL: 清掉探针之后和 A 对不上"
  command diff -u <(printf '%s\n' "$fpA") <(printf '%s\n' "$fpD") | sed 's/^/   /'
  fail=1
fi

echo
if [ "$fail" -eq 0 ]; then
  echo "ALL PASS"
else
  echo "FAILED"
fi
exit "$fail"
