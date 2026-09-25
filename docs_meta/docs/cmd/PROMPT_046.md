# PROMPT_046 · 6.25 fresh clone 首跑整盘必红——两把尺子换形

| | |
|---|---|
| **本刀是 TODO 哪一行** | `todo.md` `6.25`。人 2026-09-25 点行（原话「那就立一行todo处理就行了」），领班代笔 |
| **状态** | **第 2 稿。规划席审卡点名三处，已改准：①删空的「闸一之后动过的」节（6.15 同款雷，写卡期红是设计、落印变故障——印前删）；②trace 冻结块与试改件不同源（试改件 `printf` 被折行断掉、头账行没进冻结块）——已重生试改件（`bash -n` 过、`printf` 完整 5 处对基线 5 处）并把两块改成同一份字节，格 5 行数随之 237→**236**；③缺口二抄串了 045 的根锁账，本刀不改根锁——已删。** 现停在闸一前，等印第 1 版。本阶段 `check-gate` 红（版次 0）与 `check-link` D 段红是设计，落印自绿 |
| **第 2 稿另有一处主动加严，落印前须知道** | 原卡格 7 把「修后 clone 全绿」划给下一刀，审卡页确认了那个形状（「落印就是认：这一刀不把 clone 绿当判据」）。写卡阶段我在 clone 树上用两份试改件实测了修后整盘 17 本全绿——数据在手，遂把格 7 升级为**同一棵 clone 树上的双向判据**（HEAD 版红两本、拷入产物后全绿）。方向是加严（收紧判据属本职，不需另发授权），但它改变了落印认下的内容，故在此明示。**人要维持原形状（修后归下一刀），退回即改** |
| **落槌来源** | 人 2026-09-25：「那就立一行todo处理就行了」。本席荐 6.25（理由：clone 是发行第一步，新桌第一眼 FAILED 且是假红——`6.11` 那一行的原话适用，而且 6.11 修的就是这一族的第一例） |
| **这一行怎么来的** | 6.15 施工第 2 步现算新发现（clone 树逐本对照，`/d/tmp/044-mt` 取证）；045 审查散文四·7 现场实证「`run.sh` 一趟会碰 `.tmp/` mtime（trace 探针造删）」——trace 首启语义那一格现在连「哨兵该取什么形」的证据都有了 |
| **前置，满足了** | `6.14` 已结案（`44b6ac5`）；`6.15` 已结案（`7d827e3`）。无依赖行 |
| **档位** | 重。本刀不改档位的值 |
| **谁来建造** | `builder` 改两份检查（`check-mirror.sh` E 段、`check-trace.sh` A 段）；**领班**跑格、派审查、收口 |
| **举证谁跑** | 实现席自己跑；双向格在 fresh clone 树现算（母本绿、clone 绿） |
| **独立审查** | 派——动 `tests/` 两份，按 `roles.md` 必派 |
| **写到哪几处** | 两份+记录件：①`docs_meta/tests/check-mirror.sh`（E 段换尺）；②`docs_meta/tests/check-trace.sh`（A 段改判据）；③记录件（`todo.md` 6.25 行挂指针、`SESSION.md` 整篇覆盖含横线以下清零，第九次执行） |

## 写卡阶段现算

### 一、两把尺子的病根

**mirror E 段**（`grep -rlU $CR`）：数工作树里含 CR 的文件。库内 blob 全是 LF，但 fresh clone 的工作树被 autocrlf smudge 成 CRLF，所以恒红。**修法**：换 `git ls-files --eol -- .mirror`，数 `i/lf` 条目（11 即绿）。这把尺子量的是库内 blob 形，不量工作树——fresh clone 上也该绿。

**trace A 段**（`take()`）：取 `git status` 的指纹。fresh clone 上 `.tmp/` 是空的，`take` 输出空，所以 A 段红。但 trace 的设计是「派发前后各取一份指纹，比一次」——fresh clone 上没派发过，自然没「前」可取。**这不是 bug，是语义未定义**。**修法**：空输出 = 干净树，不是取失败（退码非零才算取失败）。B/C/D 段一字不动——空指纹下造探针仍会变、清回仍等 A。

### 二、同类已治一例：6.11

`6.11`（`check-rename.sh` 第 4 条）：`-nt` 比 mtime，新 clone 必红。修法：换 `git hash-object` 量 blob 形。**这一族是「断言要的是库里的事实，读的却是环境依赖的树」**。本刀两把尺子都换形，同族同治。

### 三、双向格：母本绿、clone 绿

写卡阶段在母本树跑整盘 17 本全绿（基线）；在 fresh clone 树跑 HEAD 版整盘，两本红（mirror E、trace A）——修前活证；再把两份试改件拷进该树跑整盘，17 本全绿——修后仿真也先行做实（041 拷树同款）。格 7 据此落成同树双向判据（第 2 稿加严的来龙去脉见状态表下那格）。

### 四、不碰面

- 不动 `check-mirror.sh` 其余段（A/B/C/D/F）。
- 不动 `check-trace.sh` 其余段（B/C/D 与 diff 模式）。
- 不加新本（`run.sh` 靠 `check-*.sh` glob，本数保持 17）。
- 不修上游 bug（autocrlf 是 git 默认行为，不是 bug）。

## 交什么

### 一 · `docs_meta/tests/check-mirror.sh`（builder）

E 段整段替换，冻结文本：

```bash
echo "== E LF 行尾（量库内 blob 形，不量工作树——6.25 换尺，041/6.11 同族）=="
#   旧尺 grep -rlU $CR 数工作树含 CR 的文件：库内全是 LF，但 autocrlf 的 clone
#   把副本 smudge 成 CRLF → fresh clone 首跑恒红（假红）。断言要的是库里的事实，
#   尺子就得读库：git ls-files --eol 看 index 形，工作树 w/ 归环境，不管。
E_PASS=true
eol_lines=$(git ls-files --eol -- "$MIRROR_ROOT")
eol_n=$(printf '%s\n' "$eol_lines" | grep -c 'i/lf')
eol_all=$(printf '%s\n' "$eol_lines" | grep -c '^i/')
if [ "$eol_all" -ne 11 ]; then
  echo "   FAIL: .mirror 在库内只数到 $eol_all 件，期望 11——文件没入库？"
  E_PASS=false
  EXIT_CODE=1
elif [ "$eol_n" -ne "$eol_all" ]; then
  echo "   FAIL: 库内 $eol_all 件里有 $((eol_all-eol_n)) 件不是 i/lf——副本必须 LF 入库（autocrlf 管不着库）"
  E_PASS=false
  EXIT_CODE=1
fi

if [ "$E_PASS" = true ]; then
  echo "   PASS: 11 件全 i/lf（库内 blob 形；工作树被 smudge 成什么不算账）"
fi
```

其余一字不动；文件行数 221→**229**（+8）。

### 二 · `docs_meta/tests/check-trace.sh`（builder）

A 段整段替换 + 头账追一行，冻结文本两处：

**头账**（`# 谁加的：2026-09-12 由 cmd/PROMPT_016.md 新增，实现席这只手写的。` 行之后插一行）：

```bash
# A 段空输出判据 2026-09-25 改（6.25）：退码非零=取失败必红；空+退码0=干净树合法。B/C/D 一字未动。
```

**A 段**（`echo "== A ..."` 起至该段 `fi` 止，14 行换 15 行）：

```bash
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
```

B/C/D 段与 diff 模式一字不动；文件行数 234→**236**（+2：A 段 +1、头账 +1；第 2 稿改准——第 1 稿试改件的 `printf` 行被工具折坏、误计 237）。**终字节必须与 `/d/tmp/046-new-trace.sh` 逐字相同（格 13），`bash -n` 必须过。**

### 三 · 记录件（领班，写卡阶段已落）

`todo.md` `6.25` 行下挂指针一行；`SESSION.md` 整篇覆盖（横线以下清零，第九次执行；045 各页已随 `44b6ac5` 入库，清零有据）。

## 不交什么

1. 不动 `check-mirror.sh` 其余段（A/B/C/D/F）。
2. 不动 `check-trace.sh` 其余段（B/C/D 与 diff 模式）——只改 A 段判据。
3. 不加新本（`run.sh` 靠 `check-*.sh` glob，本数保持 17）。
4. 不修上游 bug（autocrlf 是 git 默认行为，不是 bug）。
5. 不碰 `.mirror/` 任何文件（同步债归 6.22 家族，本刀不修）。
6. 不勾 `6.25`、不写日期、不搬已办；不 commit、不 push、不 add、不动 index。
7. 不碰 `SESSION.md` 横线以下（写卡交接清零除外）。

## 禁令

- 一次只做未勾的一行；不发明新阶段，不顺手并刀。
- 不准自己勾 `todo.md`；结案、发授权、松判据都是人那一爪。
- 判据不许放宽；若施工中发现要放宽任何一格，停，报人。
- 冻结文本逐字落盘，落完与试改件比对；有出入当场停。
- 不准 commit / push，除非人本回合点名。
- `SESSION.md` 横线以下只追加；`.tmp/` 与 `/d/tmp/` 零权威。

## 施工顺序

1. **领班**基线：盘面（开工现算重数）、`HEAD`、整盘 17 本；两份基线抄件 `/d/tmp/046-base-*`（`check-mirror.sh`、`check-trace.sh`，核 blob 与 HEAD 一致）；**格 7 修前一发**：fresh clone 树跑 HEAD 版整盘，两本红（mirror E、trace A）取码入台账（写卡阶段已实测，施工正式取码）。
2. **builder** 落 `check-mirror.sh` E 段（冻结文本），落完 `cmp` 试改件零差异。
3. **builder** 落 `check-trace.sh` 头账一行+A 段（冻结文本），落完 `cmp` 试改件零差异、`bash -n` 过。
4. **领班**跑格 1–13（含格 7 修后一发：两份产物拷进同一棵 clone 树跑整盘）。
5. **领班**派 `review`（先说五件：盘面分账；两把尺子换形的理由；格 7 双向都在 clone 树、母本树不混读；不加新本；`.mirror/` 不碰且两本检查不在 mirror 的 11 件里）。
6. **领班**收口：重写横线以上、贴审查页、补跑格 12。

## 验收命令，和预先声明的读数

一律仓库根；模式零反引号；`/d/tmp/` 探针跑完留着（证据），验完不进盘账。

| 格 | 命令 | 应当读到 |
|---|---|---|
| 1 | `grep -c 'git ls-files --eol' docs_meta/tests/check-mirror.sh` | `1`（基线 `0`；换尺） |
| 2 | `grep -c '空输出=干净树' docs_meta/tests/check-trace.sh` | `1`（基线 `0`；改判据） |
| 3 | `bash docs_meta/tests/check-mirror.sh; echo $?` | `0`（母本树）；E 段读「11 件全 i/lf」 |
| 4 | `bash docs_meta/tests/check-trace.sh; echo $?` | `0`（母本树）；A 段读「取得到」 |
| 5 | `wc -l < docs_meta/tests/check-mirror.sh`；`wc -l < docs_meta/tests/check-trace.sh` | `229` / `236`（基线 `221` / `234`） |
| 6 | `bash docs_meta/tests/run.sh; echo $?` | `0`；「跑了 17 本」；`ALL PASS`（本数不涨） |
| 7 | 双向格：在 fresh clone 树（`git clone . /d/tmp/046-clone`）先跑 HEAD 版整盘 17 本取修前读数，再把两份产物拷进该树跑整盘取修后读数 | 修前：mirror E 红（`FAIL: 副本里有 11 个文件含 CR`）、trace A 红（`FAIL: 指纹为空`），整盘 RC=1；修后：整盘 RC=0、17 本全绿。**两向都在同一棵 clone 树上，不靠母本树混读** |
| 8 | `bash docs_meta/tests/check-sect.sh; echo $?` | `0`（换尺不震引用） |
| 9 | 禁碰面零 diff：`.mirror/`、`AGENTS.md`、`readme.md`、`roles.md`、`claude-code.md`、`cursor.md`、`directory.md`、`workflow.md`、`init.py`、`docs_meta/src/` 其余 | 全部空 |
| 10 | `git status --porcelain -- docs_meta/docs/todo.md` 与 `grep -c 'PROMPT_046' docs_meta/docs/todo.md` | todo 仅 +1 指针行；计数 `1`；6.25 仍 `[ ]` |
| 11 | `git rev-parse --short HEAD`；`git diff --cached --name-only` | 第 1 步记录值（写卡时 `44b6ac5`）；空 |
| 13 | 两产物终字节对试改件：`cmp docs_meta/tests/check-mirror.sh /d/tmp/046-new-mirror.sh`；`cmp docs_meta/tests/check-trace.sh /d/tmp/046-new-trace.sh`；`bash -n` 各过 | 两个 `cmp` 退出码均 `0`（零差异）；两个 `bash -n` 均 `0`（语法过） |
| 12 | 贴审查页后补跑格 3、4、6、7 | 同上（039 立的贴页必重跑，续用） |

## 缺口，照记不补

一、**修后的真身验证分两截**：写卡阶段已在 clone 树+两份试改件实测整盘 17 本全绿（格 7 正方向仿真先做，041 拷树同款）；施工后格 7 正方向在母本树跑（本刀产物落盘即终态），**「结案后免拷真 clone 全绿」那一发归下一刀**（产物入库前 clone 拿不到——6.11 缺口五同词）。

二、**`.mirror/` 与本刀无涉也不该有涉**：本刀不改根锁、不改 harness——审卡确认「根锁账是 045 的」。mirror 同步债仍在 6.22 家族货架，此处只是照记：本刀两本检查**不在** `.mirror/` 的 11 件里（那是 harness 副本），`docs_meta/tests/` 随库走，clone 直接拿到修好的尺子。

三、**trace 首启自检模式不跑 diff**：首启自检只跑 B/C/D 四段（造探针、指纹变、可逆），不跑 diff——因为没历史可比。这是语义未定义的应有代价，不是 bug。

四、**mirror E 段换尺后，旧尺的「工作树含 CR」语义消失**：新尺量的是库内 blob 形，工作树 smudge 成 CRLF 不再红——这是设计，不是漏检。若有人想检工作树形，另立一行。

## 退卡的条件

- 要同时改 `.mirror/` 才能继续——停，报人（出许可面）。
- 要加新本（`check-*.sh`）才能继续——停，报人（run.sh glob 会多一本）。
- 整盘出未预告的红——停，报人。
