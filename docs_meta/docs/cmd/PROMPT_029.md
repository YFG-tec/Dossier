# PROMPT_029 · 2.10a 建 `.mirror/`：母本那套 harness 按一般项目的形状另抄一份

| | |
|---|---|
| **本刀是 TODO 哪一行** | `todo.md` `2.10a`。`2.10` 人 2026-09-17 裁「可拆」裂成三行，这是第一行；`2.10b` `2.10c` 都写着依赖它 |
| **状态** | 闸一之前，**第 2 稿**。红印还没落 |
| **两个「版」不是一回事** | 「稿次」数的是闸一之前改写了几回，现在是第 2 稿，`check-gate` 不看它。`check-gate` 数的是「红印版次」——印落了几回。本刀一颗印都没落，所以卡上没有闸一之后那一节，也不该有 |
| **前置** | 行上写着依赖 `2.8c`。`2.8c` 2026-09-15 结案，进了 `e862c3a`，`docs_meta/src/init.py` 在盘上。这一条满足了 |
| **后置** | `2.10b`（`init` 把 `.mirror/` 铺到宿主）和 `2.10c`（四本对着副本再跑）都写着依赖本行。**本刀不给这两行发通行证，也不做它们的任何一件** |
| **落槌来源** | 人 2026-09-17 点行，原话逐字：「写2.10a的卡」。行本身是同日人三裁（不绑母本 / 放 `.mirror` / 可拆）加甲–庚七裁落的，原话都在 `todo.md` 产物侧那一栏，本卡不抄第二份。**第 1 稿审卡之后人又裁了一件辛**，见下表 |
| **档位** | 重。人 2026-09-12 拧的，现值在 `.cursor/rules/switches.mdc`。本刀不改档位的值 |
| **谁来建造** | **领班自己落 `.mirror/` 那 11 份；派 `contract-tester` 写一本 `docs_meta/tests/check-mirror.sh`。** 理由在「谁来建造」那一节，行上点名要卡上写清的正是这一格 |
| **举证谁来跑** | 实现席自己跑。日志一律落 `/d/tmp/`，不落 `.tmp/`，不落工作树 |
| **独立审查** | 红印落下、施工报完之后派一次 `review`。射程是下面 40 格。那一页原样落盘，标出处、不摘要、不改词 |
| **写到哪几处** | 新建 `.mirror/` 11 份；新增 `docs_meta/tests/check-mirror.sh` 一本；`todo.md` 两处（写卡阶段已落）。**母本 harness 十二份、`docs_meta/src/` 十二份，零改动** |

本卡按人 2026-09-09 那句「有时候看的很费劲」收着写：一句话一个意思，能用表就用表。
卡长是因为逐行表长；那张表是施工的字面，不是说明。

## 第 1 稿到第 2 稿改了什么

规划席 2026-09-17 审卡判「放」，不挡闸，记了六条。本席在盘上逐条现算，四条落进第 2 稿。
**四十格的预先声明读数一格没动**，改的全是字面。

| 改了什么 | 原来 | 现在 |
|---|---|---|
| 人裁一件新的 | 副本抄工作树那份 `settings.json`，是本席的判断 | **人裁辛**，原话逐字落在下表 |
| 逐行表每张小表的标题 | 各份「N 行」，比 `wc -l` 多 1 | 按 `wc -l` 改正。**逐行表里的行号一个没错**，错的只是这十一个合计数 |
| 规则一头上那个 22 | 只写「处数」，被读成行数会对不上 | 写明 **22 处 / 21 行**，多出来的那一处在哪一行也点了名 |
| 副本 `AGENTS.md:17` 的措辞 | 「各加 `{{DOSSIER_SRC}}/`」，会被读成加前缀（`docs_meta` 就留在副本里了） | 「各整条换成」，字面写死 |
| 规则七添一句 | 没说末行换行 | 十一份都以换行结尾，副本照此——不然第 20 格那个 `diff` 会为「无末行换行」变红 |
| 规则六添一句 | 只写「16 处里有 6 处随旁注删了」 | 那 6 处逐处点名，施工时可核 |

规划席另外三条本席不驳，也不动卡：缺口一（庚没牙）、缺口二（嵌套规则是推的）、缺口六（逐行表不落书）。
第 5 / 28 格「树再脏一行就假红」那一条，卡上「红印落下先重数一遍」已经接住了。

## 这一刀要落成什么

母本根上那套 harness（`CLAUDE.md` + `AGENTS.md` + `.claude/` + `.cursor/`）是母本自己用的。
它里面 62 处路径写的都是 `docs_meta/...`——母本的课题就是范式本身，所以「范式的源码」和「桌自己的源码」在母本上是同一个目录。

**一般项目不是这样。** 范式的源码在子模块里，桌自己的 `src/` `tests/` `docs/` 在宿主根上。
人 2026-09-17 裁：不绑母本那份编好的 harness，另开一个副本文件夹，按一般项目的形状改完，放 `.mirror/`，进版本管理。

所以本刀交一棵 `.mirror/`，里面 11 份文件，是母本 harness 的**人工转译**：

- 路径按「出处 / 射程」两堆分家（`todo.md` 产物侧第二条那张分法）。
- 母本专属的课题、旁注拿掉；`settings.json` 删掉含 `docs_meta` 的那几条。
- 别的一个字不动。

**验的是两格**（人裁甲）：副本里 `docs_meta` 一次都不出现；副本进盘之后整盘仍 `ALL PASS`。

## 这一行已经裁死的格

| 裁 | 原话落点 | 本刀怎么落 |
|---|---|---|
| 三裁一 | 不绑母本那份编好的 harness，另开副本 | 母本 harness 一个字不动；副本另起一棵树 |
| 三裁二 | 副本放在 `.mirror` 里，进版本管理 | 目录名 `.mirror/`，不被 `.gitignore` 排掉，结案那一次 commit 带上 |
| 甲 | 两格都要 | 第一格新起一本书（`check-mirror.sh`）；第二格跑整盘 |
| 乙 | `init` 铺 `.mirror/`，动 `src/` + `tests/` | **那是 `2.10b`**，本刀不碰 `init.py` |
| 丙 | 现算相对路径，做针对性替换 | 出处指针在副本里写成占位符，相对路径 `2.10b` 铺的时候才算 |
| 丁 | `settings.json` 进副本；`host.md` 不进 | 照落。`settings.json` 删含 `docs_meta` 的 10 条 |
| 戊 | 课题三段写成空占位 | 照落，字面写在下面第二条规则里 |
| 己 | 不在母本上冒烟测 | 本刀不铺任何东西到宿主，`D:\project_init_test` 一个字不碰 |
| 庚 | 源码改一条，母本 harness 和副本同步更新 | 行上已记它没有牙。本刀不给它装牙，见缺口第一条 |
| **辛** | **`settings.json` 以工作树为准** | 见规则四。原话逐字：「以工作树为准，这65行权限管理都是宝贵经验，得放进去」 |

辛是第 1 稿审卡之后人当场裁的。规划席指出卡上第 18–20 格钉的是工作树那份脏的 `settings.json`
（相对 `HEAD` 是 `+65 −1`），不是 `HEAD`；人裁了工作树。**所以第 18–20 格的数一个不动**，
连带一件照记在缺口十一里。

**副本不能脚本生成**（`todo.md` 产物侧第三条，实测）：`docs/` `src/` `tests/` 在 harness 里既是路径也是概念名，机械替换分不开。
所以副本是领班照下面那张逐行表**一行一行抄出来的**，表就是施工的字面。

## 闸一之前要人点的三句

行上写死一句要人点：占位符长什么样。写卡时又撞出两句。**三句都是本席的判断，不是人裁的**；开工那一声落下就是认了三句，要改在闸一改。

（原来还有第四件——`settings.json` 拿工作树还是拿 `HEAD`——**人已经裁了**，进了上表的辛，不在这一节里。）

### 一、占位符是 `{{DOSSIER_SRC}}`，整条吃掉 `docs_meta/src/`

| 写法 | 副本里 `docs_meta` 还在不在 | 甲第一格 |
|---|---|---|
| `{{母本}}/docs_meta/src/roles.md` | 在，17 处 | **红** |
| `{{DOSSIER_SRC}}/roles.md` | 不在 | 绿 |

只有第二种两格同时绿，这是行上已经算过的。本席再补三条：

- 双花括号是 mustache / Jinja 那一族的占位写法，业内现成的，不是自己造的形状。`init.py` 将来一句 `str.replace` 就换得掉。
- `check-sect.sh` 的抽取器按 `/` 切、取最后一段（脚本 `:121`–`:124`，现算）。`{{DOSSIER_SRC}}/roles.md`「两席」抽出来是 `roles.md`「两席」，**`2.10c` 那一本接得住**。
- 名字里的 `SRC` 指的是范式源码那一堆，也就是子模块里的 `docs_meta/src/`，不是桌自己的 `src/`。两堆表在 `../src/naming.md`。

### 二、`todo.md` 在副本里写成 `TODO.md`

`init.py` 铺的是 `docs/TODO.md`（`:69`，现算），出处是 `../src/directory.md` 六块表。
母本 harness 写的是 `todo.md`，16 处，因为母本自己的文件就叫 `docs_meta/docs/todo.md`。
副本要跟 `init` 铺出来的那份对上，Linux 上大小写是两份文件。

所以副本里：`docs_meta/docs/todo.md` → `docs/TODO.md`；裸的 `todo.md` → `TODO.md`。
落完副本里 `todo.md` 小写 0 处，`TODO.md` 10 处。

### 三、`.mirror/` 由领班落，不派 `builder`

行上写着「新目录归谁动，角色表没写，卡上要点名」。点名在「谁来建造」那一节。

## 谁来建造

出处是 `directory.md:287`–`:291` 三只手那张表，和 `cmd/PROMPT_028.md`、`cmd/PROMPT_023.md` 两次同样的判断：

| 手 | 它那一格写死能动什么 | 本刀要动的 | 派不派 |
|---|---|---|---|
| `builder` | `docs_meta/src/`（卡片点名的）+ `.tmp/` | `src/` 一个字不动 | **不派** |
| `contract-tester` | `docs_meta/tests/` + `.tmp/` | 新增 `check-mirror.sh` 一本 | **派** |
| `review` | 写**无** | —— | 只读那一趟派 |

`.mirror/` 不在任何一只手的格里。派一只格子对不上的手去动格子外面的东西，是拿角色表当摆设。
**所以领班自己落。** 行上那句「`builder` 一只手」是行文，卡上以这一格为准。

`review` 照派。本刀没动 `docs_meta/src/`，`review.md:61` 那句「不动源码的刀不派」字面上够得着，但 62 处人工转译没有第二双眼睛就是自评，`PROMPT_028` 同样的处境也派了。

**先书后副本，先红后绿。** 顺序写死：

1. 派 `contract-tester` 写 `check-mirror.sh`。写完跑一次，`.mirror/` 还不在，**红**，日志留下。
2. 领班照逐行表落 `.mirror/` 11 份。
3. 再跑 `check-mirror.sh`，绿。
4. 整盘后台跑一趟，**跑的时候不动工作树**（`check-trace.sh` D 段会抓，`PROMPT_028` 那一刀撞过）。
5. 逐格举证，派 `review`。

## 副本长什么样：七条规则

逐行表按这七条落，表上每一行都标着用的是哪一条。

### 规则一 · 路径按两堆分家

| 母本里写的 | 处数 | 副本里写成 | 为什么 |
|---|---|---|---|
| `docs_meta/docs/` | 22 | `docs/` | 桌的在办层，`init` 铺在宿主根上 |
| `docs_meta/tests/` | 12 | `tests/` | 桌的把关层。十二处全指桌自己的把关，没有一处指母本那十五本 |
| `docs_meta/src/<文件>.md` | 17 | `{{DOSSIER_SRC}}/<文件>.md` | **出处指针**，指范式源码，留在子模块 |
| `docs_meta/src/`（裸，指桌自己的核） | 9 | `src/` | **射程指针**，指桌自己的产品源码 |
| `docs_meta/src/`（裸，按意思是出处） | 2 | `{{DOSSIER_SRC}}/` | `CLAUDE.md:9` `:51` 两处说的是「范式的源码在哪」，不是射程 |

22 + 12 + 17 + 9 + 2 = 62，和行上那个数对得上。行上写「11 处裸的 → `src/`」是原始计数，两处按意思归出处是本卡细分的。
**这张表数的一律是「处」，不是「行」。** `docs_meta/docs/` 是 **22 处 / 21 行**：
`.claude/skills/write-cmd/SKILL.md:3` 那一行的 description 里写了两处。别处都是一行一处。

22 处 `docs_meta/docs/` 里有 5 处不变成 `docs/`：`CLAUDE.md:12` 随规则二整段换掉，
`CLAUDE.md:53`、`AGENTS.md:12`、`review.md:52`、`review.md:54` 随规则三删掉。**真换成 `docs/` 的是 17 处。**

`settings.json` 里另有 10 处 `docs_meta`，归规则四单算，不在这 62 里（62 + 10 = 72，全盘现算）。

不带路径的出处引用（`workflow.md`「全程」那种，`CLAUDE.md:55`–`:76`）**一个字不动**——它们本来就不含 `docs_meta`。

### 规则二 · 课题三段写成空占位（人裁戊）

三段是 `CLAUDE.md:7`–`:9`、`CLAUDE.md:11`–`:12`、`AGENTS.md:3`–`:4`。字面写死如下，施工照抄。

`CLAUDE.md:7`–`:9` 换成：

```text
**这张桌的课题是：**（空占位。桌自己填：一句话说产物是什么、给谁用。）
范式的源码在 `{{DOSSIER_SRC}}/`，根上这些 harness 文件是从那里转译出来的产物，本页就是其中一份。
```

`CLAUDE.md:11`–`:12` 换成：

```text
**这张桌是哪一类桌：**（空占位。按 `{{DOSSIER_SRC}}/directory.md` 六块表「合同」那一行选管理类还是业务类；
选完写两句：`docs/design/` 读成哪一层，落地牵头在哪一行。）
```

`AGENTS.md:3`–`:4` 换成：

```text
这张桌的课题是：（空占位。桌自己填，和 `CLAUDE.md` 那一段同一句话，不另写第二版。）
```

「六块表」三个字留在 `directory.md` 和「合同」之间，和母本一样——紧邻 `.md` 的「」才会被 `check-sect.sh` 当出处抽走。

### 规则三 · 母本专属的旁注删掉

标准：一句话只对母本成立、换一张桌就假，删。逐处列在逐行表里，这里只记类别：

| 类别 | 处 |
|---|---|
| 「换根」 | `CLAUDE.md:3`、`switches.mdc:9` |
| 母本自己的行号、卡号、日期 | 四份角色文件末尾「`2.6b` / `2.6c` 那一行的事」、`review.md:25` 那个日期、`switches.mdc:13` 拧于和原话 |
| 母本自己的 `design/` 页 | `AGENTS.md:12` xenia、`review.md:50`–`:57` 整节 |
| 「母本…」起头的说明 | `CLAUDE.md:29` 前半、`:46` 末句、`:61` 整行、`example-report:11`–`:12` 整段 |
| 指母本根 `readme.md` | `AGENTS.md:27` |

**删旁注只删那半句，正文的规矩一个字不动。** 「这一格现在没有哨兵」留着，删的是它后面「装哨兵是 `todo.md` `2.6b` 那一行的事…」那半句。

### 规则四 · `settings.json` 删含 `docs_meta` 的 10 条（人裁丁 + 辛）

**基准是工作树那一份，不是 `HEAD`**（人裁辛）。两者差 `+65 −1`：
`HEAD` 那份是 `allow` 12 / `deny` 32，含 `docs_meta` 的只有 1 行；工作树那份是 `allow` 67 / `deny` 41，
含 `docs_meta` 的 10 行。多出来的 65 行是人 2026-09-17 自己加的只读 git 白名单和几条写形式的 `deny`。

含 `docs_meta` 的 10 条全在 `allow`：`:13`–`:20`、`:22`–`:23`。
删掉这 10 行，别的一个字节不动。副本 `allow` 57、`deny` 41。

副本必须等于「工作树那份逐行去掉含 `docs_meta` 的行」，第 20 格用 `diff` 钉死。

### 规则五 · `host.md` 不进（人裁丁）

`.mirror/.claude/host.md` 不存在。它是人自己在动的文件。

### 规则六 · `todo.md` → `TODO.md`

见「闸一之前要人点的三句」第二句。`SESSION.md` 大小写和 `init` 铺的一样，不动。

母本 16 处里有 6 处不改名，是随别的规则整句删掉的，逐处点名：
`CLAUDE.md:12`（随规则二）、`CLAUDE.md:53`、`builder.md:37`、`contract-tester.md:43`、
`review.md:36`、`spec-guard.md:37`（随规则三）。
**剩下 10 处改成 `TODO.md`**：`CLAUDE.md:33` `:57`、`builder.md:22`、`contract-tester.md:22`、
`spec-guard.md:23`、`example-report:48`、`one-slice:31` `:36`、`write-cmd:22` `:46`。

### 规则七 · LF，末行换行，别处字节一致

母本十一份盘上全是 LF，副本照此。`git add` 时 `core.autocrlf` 那句警告是这台机器的，不是仓库口径。
**十一份都以换行结尾**（现算，末字节都是 `\n`），副本照此——`settings.json` 少了这个换行，第 20 格那个 `diff` 会为「无末行换行」变红。
逐行表没点到的行，逐字节和母本相同。代码块里的对齐空格可以重排，只动空格。

## 逐行表

行号是母本 2026-09-17 盘上的。「规则」栏对上面七条。各份后面那个数是 `wc -l`。

### `CLAUDE.md`（87 行）

| 行 | 怎么改 | 规则 |
|---|---|---|
| `:3` | 「换根带走」→「由 `init` 铺到桌上」 | 三 |
| `:5` | `docs_meta/src/claude-code.md` → `{{DOSSIER_SRC}}/claude-code.md` | 一 |
| `:7`–`:9` | 整段换成规则二那两行 | 二 |
| `:11`–`:12` | 整段换成规则二那两行 | 二 |
| `:14` | `docs_meta/src/roles.md` → `{{DOSSIER_SRC}}/roles.md` | 一 |
| `:19` | `docs_meta/src/cursor.md` → `{{DOSSIER_SRC}}/cursor.md` | 一 |
| `:24` | `@.cursor/rules/switches.mdc` 不动 | 七 |
| `:28` | `docs_meta/src/directory.md` → `{{DOSSIER_SRC}}/directory.md` | 一 |
| `:29` | 整句换成「在办层是 `docs/`，把关层是 `tests/`。」 | 三 + 一 |
| `:32` | `docs_meta/docs/design/` → `docs/design/` | 一 |
| `:33` | `docs_meta/docs/todo.md` → `docs/TODO.md` | 一 + 六 |
| `:34` | `docs_meta/docs/SESSION.md` → `docs/SESSION.md` | 一 |
| `:36` `:37` | `docs_meta/tests/` → `tests/`，各一处 | 一 |
| `:43` | `docs_meta/src/workflow.md` → `{{DOSSIER_SRC}}/workflow.md` | 一 |
| `:45` | `docs_meta/docs/cmd/` → `docs/cmd/` | 一 |
| `:46` | `docs_meta/docs/design/` → `docs/design/`；末句「本桌没有合同层那一档。」删 | 一 + 三 |
| `:51` | `docs_meta/src/` → `{{DOSSIER_SRC}}/` | 一（出处） |
| `:53` | 「（`docs_meta/docs/todo.md` 里那一裁）」删，句子接成「…是哪边先动的。真要改源码，那是另一刀。」 | 三 |
| `:57` | `todo.md` → `TODO.md` | 六 |
| `:61` | 整行删 | 三 |
| 其余 | 不动 | 七 |

### `AGENTS.md`（27 行）

| 行 | 怎么改 | 规则 |
|---|---|---|
| `:3`–`:4` | 整段换成规则二那一行 | 二 |
| `:12` | 整行删；`:11` 末尾「——」改成「。」，接「所以这里只有一个指针…」 | 三 |
| `:17` | 两处**各整条换成** `{{DOSSIER_SRC}}/cursor.md`、`{{DOSSIER_SRC}}/roles.md`。**不是加前缀**——加前缀会把 `docs_meta` 留在副本里 | 一 |
| `:24` | `docs_meta/docs/` → `docs/` | 一 |
| `:27` | 「这一条在 `readme.md`」→「这一条在 `CLAUDE.md`」 | 三 |

`:27` 改指 `CLAUDE.md` 的理由：桌的根 `readme.md` 是桌自己的，那句话在它里面不会有；`CLAUDE.md:14`–`:16` 有。
不写成 `{{DOSSIER_SRC}}/roles.md`「两席」——`check-sect.sh` C 段钉着短锁里紧邻 `.md` 的「」恰好 0 处。

### `.claude/agents/builder.md`（37 行）

| 行 | 怎么改 | 规则 |
|---|---|---|
| `:3` | description 里 `docs_meta/src/` → `src/` | 一 |
| `:9` | `docs_meta/src/roles.md` → `{{DOSSIER_SRC}}/roles.md` | 一 |
| `:16` | `docs_meta/src/` → `src/` | 一 |
| `:21` | `docs_meta/tests/` → `tests/` | 一 |
| `:22` | `docs_meta/docs/todo.md` → `docs/TODO.md` | 一 + 六 |
| `:37` | 留「这一格现在没有哨兵。」，后半句删 | 三 |

### `.claude/agents/contract-tester.md`（43 行）

| 行 | 怎么改 | 规则 |
|---|---|---|
| `:3` | description 里 `docs_meta/tests/` → `tests/` | 一 |
| `:9` | → `{{DOSSIER_SRC}}/roles.md` | 一 |
| `:16` | → `tests/` | 一 |
| `:21` | `docs_meta/src/` → `src/` | 一 |
| `:22` | → `docs/TODO.md` | 一 + 六 |
| `:28` | → `tests/` | 一 |
| `:43` | 同 `builder.md:37` | 三 |

### `.claude/agents/review.md`（63 行）

| 行 | 怎么改 | 规则 |
|---|---|---|
| `:9` | → `{{DOSSIER_SRC}}/roles.md` | 一 |
| `:23` `:28` | `docs_meta/tests/` → `tests/`，各一处 | 一 |
| `:25` | 「**留 `Bash` 是人 2026-09-12 落的。**」→「**`Bash` 留着。**」 | 三 |
| `:36` | 整行删 | 三 |
| `:50`–`:57` | 整节删，含标题和节末空行 | 三 |
| `:61` | `docs_meta/src/` → `src/` | 一 |

### `.claude/agents/spec-guard.md`（37 行）

| 行 | 怎么改 | 规则 |
|---|---|---|
| `:3` | description 里 → `docs/SESSION.md` | 一 |
| `:9` | → `{{DOSSIER_SRC}}/roles.md` | 一 |
| `:16` | → `docs/SESSION.md` | 一 |
| `:21` | → `src/`、`tests/` | 一 |
| `:23` | → `docs/TODO.md` | 一 + 六 |
| `:37` | 同 `builder.md:37` | 三 |

### `.claude/skills/one-slice/SKILL.md`（38 行）

| 行 | 怎么改 | 规则 |
|---|---|---|
| `:8` | → `{{DOSSIER_SRC}}/roles.md` | 一 |
| `:21` | → `tests/` | 一 |
| `:23` `:30` `:32` | `docs_meta/src/` → `src/`，各一处 | 一 |
| `:31` | `todo.md` → `TODO.md` | 六 |
| `:36` | → `src/`、`tests/`；`todo.md` → `TODO.md` | 一 + 六 |

### `.claude/skills/example-report/SKILL.md`（48 行）

| 行 | 怎么改 | 规则 |
|---|---|---|
| `:8` | → `{{DOSSIER_SRC}}/roles.md` | 一 |
| `:9` | `docs_meta/src/verify.md` → `{{DOSSIER_SRC}}/verify.md` | 一 |
| `:11`–`:12` | 整段删，含下面那个空行 | 三 |
| `:48` | `todo.md` → `TODO.md` | 六 |

### `.claude/skills/write-cmd/SKILL.md`（48 行）

| 行 | 怎么改 | 规则 |
|---|---|---|
| `:3` | description 里两处 → `docs/cmd/PROMPT_xx.md`、`docs/SESSION.md`。**这一行是全盘唯一一行里有两处的** | 一 |
| `:8` | → `{{DOSSIER_SRC}}/roles.md` | 一 |
| `:9` | → `{{DOSSIER_SRC}}/workflow.md` | 一 |
| `:15` | → `docs/cmd/PROMPT_xx.md` | 一 |
| `:16` | → `docs/SESSION.md` | 一 |
| `:22` | → `docs/TODO.md` | 一 + 六 |
| `:46` | `todo.md` → `TODO.md` | 六 |

### `.cursor/rules/switches.mdc`（13 行）

| 行 | 怎么改 | 规则 |
|---|---|---|
| `:9` | 「换根的桌各自有一份」→「各桌各自有一份」 | 三 |
| `:13` | `\| 档位 \| 重 \| （空占位，还没拧过） \| （空占位） \|` | 三 |

值留「重」：母本现值，也是两档里紧的那一档。桌第一次拧再填另外两格。

### `.claude/settings.json`（116 行）

删 `:13`–`:20`、`:22`–`:23` 共 10 行。别的字节不动。基准是工作树那一份（人裁辛）。

## 交什么

### 第 1 件 · `docs_meta/tests/check-mirror.sh`（`contract-tester` 写）

射程**只扫 `.mirror/`**，不扫母本 harness，不扫 `D:\project_init_test`，不扫任何铺出去的宿主树。
不带根目录开关；`run.sh` 自动发现它，第十六本。零权威，只作证。

| 段 | 断言 | 期望值从哪来 |
|---|---|---|
| A | 11 件逐件在，且 `find .mirror -type f` 恰好 11 件 | 清单字面写在脚本里，出处是本卡「写到哪几处」和 `todo.md` `2.10a` 那一行 |
| B | `.mirror/` 里 `docs_meta` 0 处 | 人裁甲第一格 |
| C | 双花括号只有一种形状 `{{DOSSIER_SRC}}/`，且至少 1 处 | 本卡「闸一之前要人点的三句」第一句 |
| D | `.mirror/.claude/host.md` 不在 | 人裁丁 |
| E | `.mirror/` 里 CR 字节 0 | 规则七 |
| F | 「空占位」在 `.mirror/CLAUDE.md` 恰好 2 行、`.mirror/AGENTS.md` 恰好 1 行 | 人裁戊 |

脚本头照 `check-skel.sh` 的写法：谁加的、钉的是哪几裁、查不到什么。
**先红后绿要真演一次**：`.mirror/` 落下之前跑一趟，退出码非零，日志 `/d/tmp/029-mirror-red.log`。

### 第 2 件 · `.mirror/` 11 份（领班落）

```text
.mirror/CLAUDE.md
.mirror/AGENTS.md
.mirror/.claude/agents/builder.md
.mirror/.claude/agents/contract-tester.md
.mirror/.claude/agents/review.md
.mirror/.claude/agents/spec-guard.md
.mirror/.claude/skills/write-cmd/SKILL.md
.mirror/.claude/skills/one-slice/SKILL.md
.mirror/.claude/skills/example-report/SKILL.md
.mirror/.claude/settings.json
.mirror/.cursor/rules/switches.mdc
```

照逐行表落，一行一行来。**不 `git add`**：进版本管理读成「不被 `.gitignore` 排掉，结案那一次 commit 带上」，
施工阶段不碰 index（同 `PROMPT_028` 第 1 件那条理由）。盘面上是 11 行 `??`。

### 第 3 件 · `todo.md` 两处（写卡阶段已落）

- `2.10a` 那一行下面加卡片指针一行：`      → cmd/PROMPT_029.md`。
- `2.10a` 行里「删掉 12 条母本专属的（`docs_meta/*`），其余 8 条照抄」是本席写错的数，改成 10 条、`allow` 67 → 57。

**行首那一句原措辞一个字不改**——结案时要原样搬进已办。

## 不交什么

- **不勾 `2.10a`，不写结案日期，不往已办搬。** 那是人的一爪。
- **不 commit，不 push，不 `git add`。** 人显式说「结案」那一句才是 commit 的点名。
- **不做 `2.10b`**：不改 `init.py`，不改 `check-skel.sh`，不铺任何东西到宿主，不算相对路径。
- **不做 `2.10c`**：`check-sect.sh` `check-lock.sh` `check-role.sh` `check-switch.sh` 一本不加开关，不对着 `.mirror/` 跑它们。
- **不碰母本 harness 十二份**，包括不去改 `CLAUDE.md:3` 那句「换根带走」和四份角色文件里陈旧的「`2.6b` 那一行的事」——产物跟源码走，那是另一刀。
- **不碰 `.claude/host.md`、`.claude/settings.json`。** 都是人自己动着的；辛裁的是「照着抄」，不是「去改它」。
- **不碰 `docs_meta/src/` 任何一份**，含 `naming.md`、`directory.md`。
- **不碰现有十五本把关和 `run.sh`。**
- **不碰 `docs_meta/docs/design/`**，含人自己动着的 `ch2.md`。
- **不碰 `cmd/`** 除本卡之外的任何一份。
- **不碰 `SESSION.md` 横线以下。**
- **不碰根 `readme.md`、`.gitignore`、`example_meta/`。**
- **不碰 `D:\project_init_test`。**
- **不给庚装牙**，不加反方向的对账。
- **不做 `3.3`、`4.7`、`4.8`。不改档位的值。**

## 禁令

- **不准自己勾 `todo.md`。**
- **不准发授权**，不准放宽任何一条已经写死的判据。
- **红印之前不许落第一笔。** 人说开工那一刻，原话逐字抄进 `SESSION.md` 横线以上，印才算落下。
- **红印之后卡不许再改。** 要改走退回闸一那道手续，重提、重印。
- **不准为了让盘面好看去改任何一本把关的口径**，含新起的这一本。
- **不准让 `check-mirror.sh` 扫到 `.mirror/` 外面。** 扫到宿主树，「`docs_meta` 为 0」就是错的判据（`2.10b` 铺完那里**应该**出现 `docs_meta`）。
- **不准在逐行表之外多改一处、少改一处。** 表上没有的行，逐字节等于母本。
- **整盘在后台跑的时候不准动工作树。**
- **`.tmp/` 零权威**：日志一律落 `/d/tmp/`，不许在任何地方写「通过」。

## 验收命令，和预先声明的读数

**全部由实现席自己在盘上跑**，一格都不采信任何一只手回报的数。
带中文和反引号的探针一律 `grep -F`。`grep -r` 一律以 `.mirror` 为根。

### 一、`.mirror/` 的形状（5 格）

| 格 | 命令 | 声明的读数 |
|---|---|---|
| 1 | `find .mirror -type f \| wc -l` | **11** |
| 2 | `find .mirror -type f \| sort` | 恰好第 2 件那 11 行 |
| 3 | `test -e .mirror/.claude/host.md; echo $?` | **1** |
| 4 | `git check-ignore .mirror/CLAUDE.md; echo $?` | **1**，没被忽略 |
| 5 | `git status --short -uall \| grep -c '^?? .mirror/'` | **11** |

### 二、母本的词没进副本（8 格）

| 格 | 命令 | 声明的读数 |
|---|---|---|
| 6 | `grep -rl docs_meta .mirror \| wc -l` | **0** |
| 7 | `grep -rlF 'todo.md' .mirror \| wc -l` | **0** |
| 8 | `grep -rhoF 'TODO.md' .mirror \| wc -l` | **10** |
| 9 | `grep -rl 换根 .mirror \| wc -l` | **0** |
| 10 | `grep -rl '2026-' .mirror \| wc -l` | **0** |
| 11 | `grep -rl Dossier .mirror \| wc -l` | **0**（区分大小写；`{{DOSSIER_SRC}}` 全大写，不算） |
| 12 | `grep -rho 母本 .mirror \| wc -l` | **1**，只剩 `switches.mdc` 那句「不回流到母本」 |
| 13 | `grep -rlE '2\.6[bc]\|xenia\|paradigm' .mirror \| wc -l` | **0** |

### 三、占位符（4 格）

| 格 | 命令 | 声明的读数 |
|---|---|---|
| 14 | `grep -rho '{{DOSSIER_SRC}}/[a-z-]*\.md' .mirror \| wc -l` | **17** |
| 15 | 第 14 格加 `\| sort \| uniq -c` | `roles` 9、`workflow` 2、`directory` 2、`cursor` 2、`claude-code` 1、`verify` 1 |
| 16 | `grep -rhoF '{{DOSSIER_SRC}}/' .mirror \| wc -l` | **19**（17 + `CLAUDE.md:9` + `:51`） |
| 17 | `grep -rho '{{[^}]*}}' .mirror \| sort -u` | 恰好一行 `{{DOSSIER_SRC}}` |

### 四、`settings.json`（3 格）

**基准一律是工作树那一份**（人裁辛），不是 `HEAD`。

| 格 | 命令 | 声明的读数 |
|---|---|---|
| 18 | `grep -c docs_meta .mirror/.claude/settings.json` | **0**（母本工作树 10） |
| 19 | `python -c "import json;d=json.load(open('.mirror/.claude/settings.json'))['permissions'];print(len(d['allow']),len(d['deny']))"` | **`57 41`** |
| 20 | `grep -v docs_meta .claude/settings.json > /d/tmp/029-settings-expect.json`，再 `diff /d/tmp/029-settings-expect.json .mirror/.claude/settings.json \| wc -l` | **0** |

第 20 格钉的是规则四的字面：副本 = 工作树那份逐行去掉含 `docs_meta` 的行。
`python` 那一格用相对路径，**不喂 `/d/tmp/...` 给它**——那是 Git Bash 的路径，Windows 的 `python` 读不了。

### 五、课题三段与开关（3 格）

| 格 | 命令 | 声明的读数 |
|---|---|---|
| 21 | `grep -c 空占位 .mirror/CLAUDE.md` | **2** |
| 22 | `grep -c 空占位 .mirror/AGENTS.md` | **1** |
| 23 | `grep -c 空占位 .mirror/.cursor/rules/switches.mdc` | **1**（一行两格） |

### 六、LF 与别处没碰（8 格）

| 格 | 命令 | 声明的读数 |
|---|---|---|
| 24 | `grep -rlU $'\r' .mirror \| wc -l` | **0** |
| 25 | `git status --short -- CLAUDE.md AGENTS.md .claude .cursor` | 恰好 **2** 行，都是 ` M`：`host.md`、`settings.json`，本刀之前就在 |
| 26 | `git diff --stat -- docs_meta/src/` | **空** |
| 27 | `ls docs_meta/src/ \| wc -l` | **12** |
| 28 | `git status --short -uall -- docs_meta/tests/` | 恰好 **1** 行：`?? docs_meta/tests/check-mirror.sh` |
| 29 | `ls docs_meta/tests/ \| wc -l` | **17**（现在 16） |
| 30 | `wc -l < .gitignore` | **5** |
| 31 | `git diff --stat -- docs_meta/docs/design/` | 恰好 **1** 份：`ch2.md`，人自己的 |

### 七、书与整盘（6 格）

`bash docs_meta/tests/run.sh > /d/tmp/029-run.log 2>&1`。后台跑，跑的时候不动工作树。

| 格 | 命令 | 声明的读数 |
|---|---|---|
| 32 | `/d/tmp/029-mirror-red.log` 那一趟的退出码 | **非零**，跑在 `.mirror/` 落下之前 |
| 33 | `bash docs_meta/tests/check-mirror.sh; echo $?`（副本落完） | **0** |
| 34 | `run.sh` 退出码 | **0** |
| 35 | `grep -c '^---- .*退出码 0' /d/tmp/029-run.log` | **16** |
| 36 | `grep -c '跑了 16 本' /d/tmp/029-run.log` | **1** |
| 37 | `tail -1 /d/tmp/029-run.log` | **`ALL PASS`** |

第 35 格的正则是严口径，不许换成 `grep -c '退出码 0'`（`PROMPT_028` 第 18 格那条理由）。

### 八、卡与盘（3 格）

| 格 | 命令 | 声明的读数 |
|---|---|---|
| 38 | `grep -c PROMPT_029 docs_meta/docs/todo.md` | **1** |
| 39 | `todo.md` `2.10a` 那一行的勾选框 | 写卡落完、施工落完各看一次，两次都是 `- [ ]` |
| 40 | `bash docs_meta/tests/check-done.sh; echo $?` | **0** |

**40 格，全中才算落成。**

盘面 `git status --short -uall | wc -l` 的堆法，备查不入格：

```text
人自己动着的 3 份   .claude/host.md、.claude/settings.json、design/ch2.md
早先代落没进 commit  docs_meta/docs/cmd/README.md
写卡 3 份           本卡、SESSION.md、todo.md
                    ------  写卡落完 7
施工 12 份          .mirror/ 11 + check-mirror.sh 1
                    ------  施工落完 19
```

**红印落下那一刻先把基线重数一遍**，树多一行少一行就在运行态里说清是谁，不硬套。

## 写卡阶段盘面会红，那是设计

写卡落完、红印还没落的那一段，整盘会有两本红：

- `check-link.sh` D 段要 `SESSION.md` 横线以上有「闸一红印 + 日期」同行——红印没落就没有那一行。
- `check-gate.sh` 数红印版次——同上。

印一落它们自己转绿。所以第七组那几格**跑的时点是红印落下、施工落完之后**。
写卡阶段只跑第六组「别处没碰」和第八组「卡与盘」。

施工中还会多一段红：第 1 件落下、第 2 件还没落的那一段，`check-mirror.sh` 红。**那是先红后绿，第 32 格要的正是它。**

## 缺口，照记不补

一、**庚没有牙。** 母本源码加一条禁令、副本没跟上，本刀之后盘上一本都不会红。
`check-mirror.sh` 管的是副本自己的形状，不管它和母本对不对得上；对得上的结构验收是 `2.10c`。
反方向的对账要活过结案，落点得在 `../src/` 或一本书里，**那是另一行**，行上已经写了。

二、**`.mirror/.cursor/rules/switches.mdc` 会不会被 Cursor 当嵌套规则读进去，推的，没实测。**
读进去就是开关现值的第二份，而 `check-switch.sh` C 段用根级 pathspec，够不着 `.mirror/`。
`.mirror/.claude/` 同理，Claude Code 只读根上那一份，推的。照记。

三、**母本自己的 harness 有几句已经陈旧**：`CLAUDE.md:3`「换根带走」（人 2026-09-14 把换根清出现行舞台，产物没跟）、
四份角色文件末尾「`2.6b` / `2.6c` 那一行的事…它还没开工」（早结案了）、`review.md:36` 同。
副本里不抄，母本里不改。盘上现算没有一本把关会为这几句红。**产物跟源码走，改它是另一刀。**

四、**`src/` 的落点数没有钉。** 副本里 `src/` 既是新换上的 9 处，也是原来就有的概念名，数不干净（`todo.md` 产物侧第三条）。
本刀用「`docs_meta` 为 0」加逐行表兜。

五、**副本没法靠使唤验。** `.mirror/.claude/` 不会被会话加载（推的）。本刀只验形状，功能一致归 `2.10c`。

六、**逐行表是本卡的一次现算，不存进任何一本书或 `src/`。** 书里只存 11 件清单和几个计数，不存「母本第几行 ↔ 副本怎么写」那张映射。
存了就是禁令里那张覆盖表。

七、**`{{DOSSIER_SRC}}` 这个名是本刀起的。** `init` 铺的时候换成什么相对路径，是 `2.10b` 的事。

八、**`AGENTS.md:27` 母本自己那句在桌上会假**（「这一条在 `readme.md`」）。副本改指 `CLAUDE.md`，母本不动，同第三条。

九、**`deny` 那 41 条照抄**，含人 2026-09-17 加的那几条写形式的 `git branch -d` / `git tag -d`。一般项目要不要，人以后裁，本刀不判。

十、**`host.md` 那张前缀表和 `settings.json` 对不齐**，`PROMPT_028` 那一刀记过。人的文件，不碰。

十一、**库里会有两份对不齐的 `settings.json`，这是辛那一裁的代价，照记。**
副本抄的是工作树那份（`allow` 67 / `deny` 41），母本 `.claude/settings.json` 在 `HEAD` 上还是 `allow` 12 / `deny` 32，
那 65 行人加了一直没进 commit。结案那一次要是只带 `.mirror/`，库里两份就差 65 行。
**要不要把 `.claude/settings.json` 一起带进那一次 commit，是人的那一爪**，本刀不碰它，也不替人决定。

## 退卡的条件

触发任何一条，当场退卡，不在核上折衷：

- **落副本时发现有一处路径既分不进出处也分不进射程**，逐行表分不了家。退卡，让人裁那一处。
- **副本落完 `docs_meta` 不为 0，且剩下那一处按七条规则处理不了。**
- **发现要动母本 harness 任何一份才做得完。**
- **发现要动 `docs_meta/src/`（含 `init.py`、`naming.md`）才做得完。**
- **发现要动现有十五本把关或 `run.sh` 才做得完。**
- **`.mirror/` 落下之后原有十五本有一本红，而红的原因不是错字**，是那一本真的扫到了 `.mirror/`。
  退卡，不去改那一本的口径，也不去改 `.mirror/` 的位置。
- **`check-mirror.sh` 写不出「只扫 `.mirror/`」**，非扫别处不可。
- **`settings.json` 删完 10 行不是合法 JSON。**
- **施工前 `.claude/settings.json` 的工作树内容变了**（人又改了一次），第 19 / 20 格的数跟着变。
  退回闸一，重数、改卡、重提。
- **红印之后人对「闸一之前要人点的三句」任何一句再说一次话，而说的话让某一格的预先声明读数变了。**
  退回闸一：改卡、重写 `SESSION.md` 横线以上、等人重说一次开工，红印重落一次。
