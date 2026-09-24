# PROMPT_041 · 6.11 check-rename 第 4 条：扔了 mtime，改认内容戳

| | |
|---|---|
| **本刀是 TODO 哪一行** | `todo.md` `6.11`。第 6 章（历史 bug）队列头名，人 2026-09-24 按「最前置」裁出并点行 |
| **状态** | **第 3 稿。退回闸一改卡重提，等重落印（第 2 版）。** 第 2 稿施工中 builder 挖出 EOL 雷（裸字节哈希不跟 git 旅行），人裁「选A」换 `git hash-object` 尺；改动记在「闸一之后动过的」。**本阶段 `check-gate` 红是设计**：版次 1 与改动节并存，重落印第 2 版即转绿 |
| **落槌来源** | 人 2026-09-24：「我想优先处理bug…有依赖关系就解决最前置的」→ 本席荐 6.11（理由链在聊天，摘要进现算一）→「写6.11的卡」 |
| **这一行怎么来的** | 36 桌反馈 #2 收件。行内已记：`3.3` 换过比较对象，`-nt` 机制仍在 |
| **前置，满足了** | 无依赖行。`4.11` 统合已结（队列就位）。`.venv/` 在役（`3.3` 建），出图可重跑 |
| **档位** | 重。本刀不改档位的值 |
| **谁来建造** | 三只手：`builder` 改 `src/figures/make_frame.py`（戳写出）；`contract-tester` 改 `check-rename.sh` 第 4 段；**领班**跑 clone 复现与全部格。戳文件由重渲**产生**，无人手写 |
| **举证谁来跑** | 实现席自己跑；复现与仿真日志落 `/d/tmp/`（`041-repro.log`、`041-fresh.log`、`041-falsify.log`） |
| **独立审查** | 派——本刀动 `src/`（出图脚本），按 `roles.md` 必派 |
| **写到哪几处** | 三份：`docs_meta/src/figures/make_frame.py`（尾部加戳写出）、`docs_meta/src/figures/dossier-frame.render-stamp`（新增，重渲产物、随库）、`docs_meta/tests/check-rename.sh`（第 4 段重写+头账）。别的不沾 |

## 写卡阶段现算

### 一、bug 在本机新 clone 上当场复现（2026-09-24，未改一字之前）

`git clone . /d/tmp/041-repro` 后跑该树 `check-rename.sh`：第 4 段原样输出
`FAIL: PNG 旧于或同龄于出图脚本 —— 跑 make_frame.py` + `FAILED`。
**两点都钉死了**：①必红是真的、可复现；②行里「FAIL 给的处置是错的」也是真的——那句让人去跑 `make_frame.py`，可 PNG 根本没旧，重渲完 clone 一次照样同龄照红。**一个让每张新桌第一眼就学会忽略 FAILED 的检查，比没有检查更坏**——这就是它排最前的全部理由。

### 二、戳值不许冻进格（6.6 病本刀不犯第三次）

builder 给 `make_frame.py` 加尾段后，脚本哈希**必然改变**；戳内容=改后脚本的现算值。所以第 4 号格的写法是**两侧同式现算比对**，不是卡上预先抄一串定值。第 1 稿时代算得的 sha256 `5903b5fd…` 只是改前基线证物；第 3 稿换尺后连证物也换了族（blob 哈希），更不许冻。

### 三、尺子与解释器（第 3 稿，人裁 A 后重写）

- **比对用 `git hash-object`**：算的是 git 眼中内容（blob 哈希，入库归一化后），**对 EOL 形态恒等**——第 2 稿施工实测：同一份 HEAD 内容，裸 sha256 两形态 `5903b5fd…`≠`0e9ae89f…`（必假红），`git hash-object` 两形态同为 `0e3eaeaa…`。检查端就此**零 python 依赖**——新桌必有 git（产品经 git 发行），未必有 python。
- **重渲仍用 `.venv/Scripts/python.exe`**：matplotlib 在它里面（`3.3` 立的）。FAIL 文案照此写处方，不再指错路。

### 三之二、EOL 雷的完整账（第 2 稿施工挖出，人裁 A）

本机 `core.autocrlf=true`、全库无 `.gitattributes`：同一份代码，库里 LF、Windows clone 工作树 CRLF。裸字节指纹不跟 git 旅行——「新 clone 必红」会换载体复活，而 clone 正是产品分发第一步。builder 实测 clone 树脚本 sha256 与戳不符后**停手上报未自采**；三条出路（A 换 git 尺 / B 加 attributes / C 降级判据）摆给人，**人 2026-09-24 裁「可以，选A」**。B 的代价（第四份文件、逐文件打地鼠、检查仍依赖 python）与 C 的代价（违 6.11 本意）都在 SESSION 台账里。

### 四、只治 frame，不顺手治 icon

第 4 段只管 `dossier-frame.png`/`make_frame.py`；`render_icon.py` 一对**不沾**（它不在本条射程，`3.3` 的格自有账）。报告建议的另一路「移出 `run.sh`」不采：规则原意「改了图脚本必须重渲」是要在入口拦得住的，错的从来不是规则，是拿 mtime 当尺。裁果要翻这条，退卡。

## 交什么

### 一 · `docs_meta/src/figures/make_frame.py`（builder）

紧接 `print(f'Generated: {output_path}')` 之后追加，冻结代码（第 3 稿，人裁 A：**整段替换第 2 稿已落盘的 sha256 尾段**，397–404 行一带）：

```python

# 6.11：渲染成功即盖内容戳——记「哪一版脚本生成了当前图」的 git 眼中哈希（blob）；
# 对 EOL 形态恒等（autocrlf 的 clone 树算出同值），git 带得走，mtime 和裸字节都带不走
import subprocess as _sp
_bh = _sp.run(['git', 'hash-object', __file__], capture_output=True, text=True, check=True).stdout.strip()
with open('docs_meta/src/figures/dossier-frame.render-stamp', 'w', newline='\n') as _s:
    _s.write(_bh + '\n')
print(f'Stamped: {_bh[:12]}…')
```

`check=True`：git 不在或算不出就当场炸，不许静默漏戳。脚本须从仓库根跑（`__file__` 相对形与它写 PNG 的路径同款）。

### 二 · 重渲（builder 或领班，一次）

`.venv/Scripts/python.exe docs_meta/src/figures/make_frame.py` 跑一次：PNG 重出、戳落地。**PNG 字节变不变都不是判据**（不比字节，比戳），变了就让它 M 着。

### 三 · `docs_meta/tests/check-rename.sh`（contract-tester）

第 4 段整段替换，冻结口径：

```bash
echo "== 4. 帧图脚本改了必须重渲（git 内容戳，不比 mtime——2026-09-24，6.11/反馈#2，闸一退卡裁 A） =="
source=docs_meta/src/figures/make_frame.py
stamp=docs_meta/src/figures/dossier-frame.render-stamp
if [ ! -f "$stamp" ]; then
  echo "   FAIL: 戳不在 —— 先跑 .venv/Scripts/python.exe docs_meta/src/figures/make_frame.py"; fail=1
else
  now=$(git hash-object "$source")
  want=$(tr -d '\r' < "$stamp")
  if [ "$now" = "$want" ]; then
    echo "   PASS: 脚本的 git 眼中哈希与戳一致，图出自当前版脚本"
  else
    echo "   FAIL: 脚本改过而图未重渲（现算与戳不符）——跑 .venv/Scripts/python.exe docs_meta/src/figures/make_frame.py，戳与图一起提交"; fail=1
  fi
fi
```

`tr -d '\r'` 不是装饰：戳文件自己也会被 autocrlf 的 clone smudge 成 CRLF，不剥 `\r` 就是「哈希对了、行尾输了」的冤红。

脚本头「第 3、4 条指针改向」那条之后**追加一行账**（不删旧账）：第 4 条 2026-09-24 从 `-nt` 换 git 内容戳，理由两条=mtime 不进 git（36 桌 #2）、裸字节也不跟 git 旅行（autocrlf 的 EOL 归一化，本刀施工实测）；尺子取 `git hash-object`，检查端零 python 依赖——新桌必有 git。

### 四 · 记录件（写卡阶段已落）

`todo.md` `6.11` 行下挂本卡指针。

## 不交什么

1. 不动 `check-rename.sh` 第 1、2、3 段与脚本头其余部分。
2. 不沾 `render_icon.py`、两张 icon 图；不沾 `.mirror/`、`init.py`、`run.sh`。
3. 不把第 4 段移出 `run.sh`（报告另一案，本刀不采；翻案退卡）。
4. 不改 `6.11` 行内容（队列行，结案才勾）；不动其余队列行。
5. 不 commit、不 push、不 `git add`；不动 index。
6. 不碰 `SESSION.md` 横线以下（写卡交接清零除外——第四次执行）。
7. 不删改旧 FAIL 文案之外的任何文案；旧处方那句随第 4 段替换自然退场，**别处不搜「跑 make_frame.py」**。
8. 不把戳 hex 写进任何格或卡正文当判据（现算二）。

## 禁令

- 一次只做未勾的一行。
- 不准自己勾 `todo.md`。
- **戳只许由渲染产生，不许手捏**——手捏的戳是假绿的第二真相。
- 判据不许放宽：第 4 段以外的一切读数保持原样；新旧 clone 两向必须都有实证（修后 clone 绿、仿真改脚本必红）。
- 不准 commit / push，除非人点名。
- `SESSION.md` 横线以下只追加；`.tmp/` 零权威。

## 施工顺序

1. **领班**基线：盘面（**开工现算重数**，写卡时实测 9 行，不拿旧数去凑）、`HEAD`、整盘 17 本；`check-rename.sh`、`make_frame.py` 抄 `/d/tmp/041-base-*`；**改前复现**：干净 clone 跑该树 check-rename，`FAILED`+退出码 `1` 记入 `/d/tmp/041-repro.log`（写卡已见红，正式取码）。
2. **builder** 落第一段（第 3 稿冻结代码，**整段替换第 2 稿已落盘的 sha256 尾段**）。
3. **领班或 builder** 重渲一次，戳落地（内容=blob 哈希）；`git status` 上 PNG 若变如实入台账。
4. **contract-tester** 落第三段（冻结口径+头账），默认根自跑 check-rename 绿。
5. **领班**跑第 1–15 格（含两个新 clone、仿真与 EOL 单元证）。
6. **领班**派 `review`（先说五件：盘面分账/旧 clone 复现的读码方式；mtime 规则；戳=渲染产物非手写、比对用裸 python 是刻意的；PNG 字节可能变、非判据；整盘 17 本、`SECT_ROOT` 既有红归 4.10 卡账）。
7. **领班**收口重写横线以上、贴审查页、补跑整盘。

## 验收命令，和预先声明的读数

一律仓库根；模式零反引号；格 7–9 的 clone 都在 `/d/tmp/` 下，跑完即删。

| 格 | 命令 | 应当读到 |
|---|---|---|
| 1 | `grep -c -F '-nt "$source"' docs_meta/tests/check-rename.sh` | `0`（基线 `1`，旧尺子退场） |
| 2 | `grep -c -F 'render-stamp' docs_meta/tests/check-rename.sh` | `≥2`（段内变量+头账） |
| 3 | `grep -c -F 'render-stamp' docs_meta/src/figures/make_frame.py` | `1`（写戳处） |
| 4 | 两侧同式现算：戳内容（`tr -d '\r'` 后）vs `git hash-object docs_meta/src/figures/make_frame.py` | **等**（不预抄定值） |
| 5 | `bash docs_meta/tests/check-rename.sh; echo $?` | `0` + `ALL PASS` |
| 6 | `git status --porcelain -- docs_meta` 三路径合读（figures 两文件+tests 一份） | 恰 `3` 行：` M` make_frame、` M` check-rename、`??` 戳（PNG 若 ` M` 为第 4 行，记台账不算红） |
| 7 | 改后靶场景：`git clone` 到 `/d/tmp/041-fresh`（checkout 天然把 PNG 与脚本落成同龄——这正是原 bug 的形状），再把本刀三份产物**拷进该树**（`make_frame.py`、`dossier-frame.render-stamp`、`check-rename.sh`；审卡点破：产物结案前未入库，clone 只有 HEAD），跑该树 check-rename | `RC=0`——内容戳在同龄形状下绿。结案后的干净 clone 无需拷贝即全绿，两形同判据 |
| 8 | 仿真（就在该 clone 树内）：给拷入的 `make_frame.py` 追加一行注释 → 跑 → 还原再跑 | 红→`RC=1` 点名「现算与戳不符」；复绿→`0`。**原罪仍抓得住** |
| 9 | 处方文案：`grep -c -F '.venv/Scripts/python.exe' docs_meta/tests/check-rename.sh` | `≥2`（两条 FAIL 文案都给对路处方） |
| 15 | **EOL 恒等单元证**（A 尺的实证）：`python -c "d=open('docs_meta/src/figures/make_frame.py','rb').read();open('/d/tmp/041-eol-crlf.py','wb').write(d.replace(b'\n',b'\r\n'))"` 造 CRLF 变体，比 `git hash-object --path=docs_meta/src/figures/make_frame.py /d/tmp/041-eol-crlf.py` 与 `git hash-object docs_meta/src/figures/make_frame.py` | 两值**等**——同内容两种行尾形态同 blob；验完变体删掉 |
| 10 | `bash docs_meta/tests/run.sh; echo $?` | 17 本 `ALL PASS` `0` |
| 11 | `check-gate`/`check-link`/`check-done`/`check-ask` 各退码（落印后） | 全 `0`；`check-ask` 对本卡读「无节——这一刀没有请示」第三次在岗 |
| 12 | `git diff --name-only -- docs_meta/src` | 仅 `figures/make_frame.py` 一份 |
| 13 | `git rev-parse --short HEAD`；`git diff --cached --name-only` | 第 1 步记录值；空 |
| 14 | 贴审查页后补跑格 10 | 同上（039 立的贴页必重跑，续用） |

## 闸一之后动过的

- 2026-09-24，第 1 版印后施工中：builder 实测挖出 EOL 雷——`core.autocrlf=true` 下新 clone 的脚本裸字节 sha256 ≠ 戳，「新 clone 必红」换载体复活；builder 停手上报未自采，三条出路（A 换 git 尺 / B 加 `.gitattributes` / C 降级判据）摆给人，**人裁原话逐字：「可以，选A」**。改动：交什么一、三两段冻结文本整段换 `git hash-object` 尺（戳读侧加 `tr -d '\r'` 护 smudge），格 4 公式随之，新增格 15（EOL 恒等单元证），现算二、三重写并增三之二记全账，施工第 2 步注明替换已落盘的 sha256 尾段。判据的意未动：两向实证（靶场景转绿 + 原罪仍抓得住）一个没少。等重落印第 2 版。

## 缺口，照记不补

一、**戳信的是「渲染那次跑的脚本=当前脚本」**——若有人改脚本后本地跑一次、只提交脚本不提交戳，红；只提交戳不提交脚本，也红；**两样一起提交而未真重渲图**，戳对图旧，绿。戳防的是漂移与 clone 必红，不防「渲染作弊」——那是 `4.10` 附注同款「形状≠诚意」边界。
二、**图字节与脚本的一致性本刀不验**（真验=现场重渲再比字节，分钟级、且绑死 matplotlib 版本——发布端那道账，不是入口的）。
三、`.venv` 路径写死在文案里，别桌若无 `.venv/` 自跑会撞空——处方文案是母本机形状；产品化归 6.19 那条队列。
四、**A 尺的极端情形**：若哪张桌在子模块里自加 attributes 把脚本标成 binary，EOL 归一化即关、两态又不等——那是桌改母本内容，本就出界（`form.md` §5 那类「限制不了，不强求」），照记不护。
五、**「结案后干净 clone 免拷即全绿」在结案前无法全真验证**（产物未入库，clone 拿不到）；格 15 单元证 + 格 7 拷树证合起来是它的机理证明，真身验证归结案后的下一次干净 clone（36 桌复验 6.16/6.19 时顺路）。

## 退卡的条件

- 改前 clone 复现不出红（基线格读不到 `FAILED`）——停，报人：靶子变了。
- 仿真格 8 抓不住（改了脚本仍绿）——停，报人：新尺子是虚的，宁可退回。
- 要动第 1–3 段、icon、`.mirror/` 或把第 4 段移出 `run.sh` 才能继续——停，报人（均出许可面）。
- 整盘出未预告的红——停，报人（`SECT_ROOT=.mirror` 那发既有红除外，账在 `4.10` 卡第 22 格）。
