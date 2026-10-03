# PROMPT_048 · 5.3 可盖谓词成命令——check-verdict.sh v1

| | |
|---|---|
| **本刀是 TODO 哪一行** | `todo.md` `5.3`。人 2026-10-02 立案（原话「除非有阶段性结果或关键性决断，日常的开发流程人不再参与(自动发印)」），代理席代笔落行；同回合人授权宽松、点序列 #1（见 `queue.md`） |
| **状态** | **第 2 稿。** 第 1 稿落印后自测拌住建造：冻结块 G0 卡路径缺 `docs_meta/docs/` 前缀（夹具暴露，母本同样会死）——退回闸一改卡重提，痕在卡「闸一之后动过的」 |
| **落槌来源** | 人 2026-10-02 序列授权，`docs_meta/docs/queue.md` #1 |
| **前置，满足了** | 无依赖行。绊线红已先治（五份旧检查源挪 `.tmp/archive/`，巡查 #1 发现二，非本刀件） |
| **档位** | 重。本刀不改档位的值 |
| **谁来建造** | `builder` 写 `docs_meta/tests/check-verdict.sh`（从本卡冻结块抽出，字节同源）；**领班**跑格、派审查、收口 |
| **举证谁跑** | 实现席自己跑；日志落 `/d/tmp/048-*.log` |
| **独立审查** | 派——本刀产出把关层自身的新成员。把关的把关必须独立：假谓词比没有谓词更危险（驯化风险，`later.md` 附三 §五），审查零写权限按 `roles.md` |
| **写到哪几处** | ①新本 `docs_meta/tests/check-verdict.sh`；②记录件 `todo.md`（5.3 行尾挂指针，施工时挂）；③记录件 `SESSION.md`（整篇覆盖，横线以下清零）；④`queue.md` 状态格 |

## 现状（builder 会踩的，开干前读）

1. **施工顺序**：脚本先建，跑格 2（此时 SESSION 仍是 047 旧案，直跑应判「已结」）；**然后**才重写 SESSION，再跑格 4（应判「在办」）。顺序反了格 2 就没有证据。
2. 脚本判「已结」读的是 `todo.md` 已办区，不读 git log——历史树的 commit 时间不进判定。
3. `run.sh` 本数 17→18 是 5.3 行声明过的改动（代笔留痕）；审查若遇旧口径「本数不涨」（6.20 卡），不适用本刀。
4. 自测全程住在 `mktemp -d` 与 `git archive` 抽出的临时树；母本树零写入（`check-trace` 绿是旁证）。
5. 本机跑检查用 `D:\Tools\Git\bin\bash.exe`（WSL shim 跑不动 CRLF，巡查 #1 发现一）。

## 交什么 · 冻结块（builder 原样抽出落盘，一个字节不改）

```bash
#!/usr/bin/env bash
# check-verdict.sh —— 可盖谓词 v1（todo 5.3，cmd/PROMPT_048，2026-10-02）
# 只读查询：这一刀走到哪一档。判定在 stdout 机器行；退出码只答自身健康（fail-closed）。
#   verdict=在办  印未落或验收未齐——队列不动
#   verdict=可盖  读数齐，可代笔结案（5.4 落地后启用）
#   verdict=断点  要人：请示在场 / 审查判返工
#   verdict=已结  行已勾、已办有本卡指针
# 读不了盘（文件缺、行抓不到）退出码 1，绝不输出可盖。
# 用法：bash docs_meta/tests/check-verdict.sh [--selftest] [--run-log <文件>]

set -u
cd "$(dirname "$0")/../.."

SESS=docs_meta/docs/SESSION.md
TODO=docs_meta/docs/todo.md

run_log=""
selftest=0
while [ "$#" -gt 0 ]; do
  case "$1" in
    --selftest) selftest=1 ;;
    --run-log) shift; run_log="${1:-}" ;;
    *) echo "G0: 不认的参数 $1"; exit 1 ;;
  esac
  shift
done

# ---------- 自测 ----------
if [ "$selftest" -eq 1 ]; then
  tmp=$(mktemp -d)
  trap 'rm -rf "$tmp"' EXIT
  fx_make() {
    fx="$1"; stamp="$2"; ask="$3"; conc="$4"
    mkdir -p "$fx/docs_meta/docs/cmd" "$fx/docs_meta/tests"
    cp docs_meta/tests/check-verdict.sh "$fx/docs_meta/tests/"
    printf -- '- [ ] **5.3** 可盖谓词成命令（夹具）\n' > "$fx/docs_meta/docs/todo.md"
    {
      printf '# 本刀运行态\n\n'
      printf '| **许可面** | [本刀卡片](cmd/PROMPT_048.md) |\n\n'
      if [ "$stamp" = 1 ]; then printf '闸一红印 · 2026-10-02 · 第 1 版\n\n'; fi
      if [ "$ask" = 1 ]; then printf '## 要人点的请示\n\n- 待人\n\n'; fi
      printf -- '---\n\n'
      if [ -n "$conc" ]; then printf '## 审查\n\n**结论：%s**\n\n' "$conc"; fi
    } > "$fx/docs_meta/docs/SESSION.md"
    printf '| **本刀是 TODO 哪一行** | `todo.md` `5.3`（夹具） |\n' > "$fx/docs_meta/docs/cmd/PROMPT_048.md"
  }
  expect() {
    fx="$1"; want="$2"; shift 2
    got=$(bash "$fx/docs_meta/tests/check-verdict.sh" "$@" | grep -oE 'verdict=[^[:space:]]+' | head -n1)
    got="${got#verdict=}"
    if [ "$got" = "$want" ]; then echo "SELFTEST: $want OK"; else echo "SELFTEST: 期望 $want 实得 ${got:-空}"; SELF_FAIL=1; fi
  }
  SELF_FAIL=0
  fx_make "$tmp/a" 1 0 "格全过，无返工"
  printf 'run log\n' > "$tmp/a/run.log"
  expect "$tmp/a" 可盖 --run-log "$tmp/a/run.log"
  fx_make "$tmp/b" 1 1 "格全过，无返工"
  expect "$tmp/b" 断点
  fx_make "$tmp/c" 1 0 "格 3 未过，返工"
  expect "$tmp/c" 断点 --run-log "$tmp/c/run.log"
  fx_make "$tmp/d" 0 0 "格全过，无返工"
  expect "$tmp/d" 在办 --run-log "$tmp/d/run.log"
  for c in 1e9f8d2 a2c5c6f; do
    w="$tmp/h-$c"
    mkdir -p "$w"
    git archive "$c" | tar -x -C "$w"
    cp docs_meta/tests/check-verdict.sh "$w/docs_meta/tests/"
    expect "$w" 已结
  done
  if [ "$SELF_FAIL" -eq 0 ]; then echo "SELFTEST PASS"; exit 0; fi
  echo "SELFTEST FAIL"
  exit 1
fi

# ---------- 正跑 ----------
[ -f "$SESS" ] || { echo "G0: SESSION.md 缺"; exit 1; }
[ -f "$TODO" ] || { echo "G0: todo.md 缺"; exit 1; }

card_path=$(grep -oE 'cmd/PROMPT_[0-9]+\.md' "$SESS" | head -n 1)
[ -n "$card_path" ] || { echo "G0: SESSION 无许可面指针"; exit 1; }
CARD_FILE="docs_meta/docs/$card_path"
[ -f "$CARD_FILE" ] || { echo "G0: 卡缺：$CARD_FILE"; exit 1; }
echo "G2: 卡=$CARD_FILE"

row_line=$(grep -F '本刀是 TODO 哪一行' "$CARD_FILE" | head -n 1)
row_id=$(printf '%s\n' "$row_line" | grep -oE '[0-9]+\.[0-9]+' | head -n 1)
[ -n "$row_id" ] || { echo "G0: 卡里抓不到行 id"; exit 1; }
row_esc=$(printf '%s\n' "$row_id" | sed 's/\./\\./')
row_in_todo=$(grep -E "^- \[.\] \*\*$row_esc\*\*" "$TODO" | head -n 1)
[ -n "$row_in_todo" ] || { echo "G0: todo 里找不到行 $row_id"; exit 1; }
echo "G3: 行=$row_id"

verdict=在办
case "$row_in_todo" in
  '- [x]'*)
    if grep -qF "$card_path" "$TODO"; then
      verdict=已结
    else
      echo "G0: 行已勾但已办无本卡指针"
      exit 1
    fi
    ;;
esac

if [ "$verdict" != 已结 ]; then
  if grep -qE '闸一红印 · [0-9]{4}-[0-9]{2}-[0-9]{2} · 第 [0-9]+ 版' "$SESS"; then
    echo "G1: 印在场"
    stamp=1
  else
    echo "G1: 印未落"
    stamp=0
  fi
  upper=$(sed '1,/^---$/!d' "$SESS")
  if printf '%s\n' "$upper" | grep -q '## 要人点的请示'; then
    echo "G5: 请示节在场"
    verdict=断点
  fi
  if [ "$verdict" != 断点 ]; then
    conc=$(sed '1,/^---$/d' "$SESS" | grep -A6 '^## 审查' | grep '结论' | head -n 1)
    if [ -n "$conc" ]; then
      echo "G4: $conc"
      is_break=0
      case "$conc" in
        *返工*) case "$conc" in *无返工*) ;; *) is_break=1 ;; esac ;;
      esac
      if [ "$is_break" -eq 1 ]; then
        verdict=断点
      elif [ -n "$run_log" ] && [ -f "$run_log" ]; then
        verdict=可盖
      else
        echo "G4: 可盖需 --run-log（v1 边界，5.4 收紧）"
      fi
    else
      echo "G4: 审查页无结论行"
    fi
  fi
  if [ "$stamp" -eq 0 ] && [ "$verdict" != 断点 ]; then
    verdict=在办
  fi
fi

echo "G6: 盘面"
if git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  git status --porcelain | sed 's/^/G6: /'
else
  echo "G6: 非库树，跳过"
fi

echo "verdict=$verdict"
exit 0
```

## 闸一之后动过的

- 第 2 稿（2026-10-02）：冻结块 G0 的卡路径缺 `docs_meta/docs/` 前缀——夹具自测暴露（子跑 `G0: 卡缺`），母本树直跑同样会死；`card_path` 判存改经 `CARD_FILE`。自测拌住建造，先修再续

## 不交什么

- 不改其余 17 本检查的任何一段；不动 `run.sh`（本数是 glob 现算，17→18 是自然结果）。
- 不动 `src/` 一个字——`roles.md` / `workflow.md` / `directory.md` 的口径归 `5.4`。
- 不删 `.tmp/archive/`；不做除格子判据外的任何「通过」宣告；本本只出判定，不落任何印。
- 不 commit、不 push。

## 禁令

- fail-closed 不许反向：读不了盘就退出码 1，任何路径不得把读不了盘输出成「可盖」。
- 夹具不许喂记死的答案：夹具文件从真实文件形生成（本卡冻结块内即生成器），不许在脚本里特判自测路径。
- 判据只许收紧；放宽任何一格即断点，呈人。

## 验收命令（工作目录 = 项目根；bash 用 `D:\Tools\Git\bin\bash.exe`）

| 格 | 命令 | 应当读到 |
|---|---|---|
| 1 | `bash docs_meta/tests/check-verdict.sh --selftest` | `SELFTEST PASS` ×1；`OK` ×6；退出码 `0` |
| 2 | `bash docs_meta/tests/check-verdict.sh > /d/tmp/048-verdict-pre.log; echo $?`（SESSION 重写**前**跑） | `verdict=已结` ×1；`0` |
| 3 | `bash docs_meta/tests/run.sh` | `跑了 18 本`；`ALL PASS`；退出码 `0` |
| 4 | `bash docs_meta/tests/check-verdict.sh > /d/tmp/048-verdict-post.log; echo $?`（SESSION 重写**后**跑） | `verdict=在办` ×1；`0` |
| 5 | `grep -c 'cmd/PROMPT_048.md' docs_meta/docs/todo.md` | `1` |
| 6 | `grep -c '^- \[ \] \*\*5\.3\*\*' docs_meta/docs/todo.md` | `1` |
| 7 | `git status --porcelain` | 行集 ⊆ {check-verdict.sh(新)， todo.md， SESSION.md， queue.md}，无多余 |
| 8 | `bash docs_meta/tests/check-trace.sh` | 退出码 `0`（母本树零写入旁证） |

## 闸一请示

（无。本刀判据已死在行里与卡上；序列授权在 `queue.md`。）
