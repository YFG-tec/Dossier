# PROMPT_057 · 6.23 「验不了什么」总账节——Codex 执行席首演

| | |
|---|---|
| **本刀是 TODO 哪一行** | `todo.md` `6.23`：母本能机械验的比它以为的少——「验不了什么」清单没有总账 |
| **状态** | 第 1 稿 |
| **落槌来源** | 人 2026-10-02 点名「本刀起用 Codex CLI 当执行席试运行」＋「继续你的开发工作」 |
| **前置，满足了** | 细则已迁 `design/lean-rows.md#6.23`（36 桌八行清单在 `reports/dossier-feedback-2026-09-17.md` 第三节）；Codex 通道探针 ALIVE |
| **档位** | 重（动 `verify.md` 条文）。本刀不改档位的值 |
| **谁来建造** | **`codex exec`（实现席·Codex，首演）**：读本卡＋材料，写 `verify.md` 新节；**领班**（代理席）写卡、落印、跑格、派审查、收口 |
| **独立审查** | 派——动条文必派 |
| **写到哪几处** | ①`docs_meta/src/verify.md`（新节「本套验不了什么」）；②记录件 |

## 给 Codex 的施工指令（领班代写的调用形状）

```powershell
$env:PATH += ";$env:APPDATA\npm"
codex exec --skip-git-repo-check -c sandbox_mode="workspace-write" "你是 Dossier 母本的实现席 builder。先读 docs_meta/docs/cmd/PROMPT_057.md（本刀卡片，唯一许可面），再读 docs_meta/docs/design/lean-rows.md 的 6.23 节与 docs_meta/docs/reports/dossier-feedback-2026-09-17.md 第三节（36 桌八行清单）。然后只做一件事：在 docs_meta/src/verify.md 末尾加一节「## 本套验不了什么（→ harness）」，把八行收拢成总账——每行一行一条：验不了什么（现象一句）＋对应 todo 行号回链＋出路一句（该谁/该哪刀）。要求：不删 verify.md 任何既有内容；新节放文件最末；中文；每行必须带 `6.x` 行号回链；写完输出你加的行数。不 commit、不碰其他文件。"
```

**验收由领班跑**（Codex 只施工）；Codex 的输出全文落 `/d/tmp/057-codex-log.md`（树外）。

## 现状（builder 会踩的）

1. `verify.md` 现无此节；节名带 `（→ harness）` 后缀会进 `check-sect` 射程——**根锁须有出处才不红**：本刀同步在根 `CLAUDE.md` 先读顺序「写报告先读」那行末尾加「＋`verify.md` 验不了什么总账」半句（转译落点），`check-sect` B 段要求 `<文件名>.md「<节名>」` 形——根锁写 `verify.md「本套验不了什么」` 即满足。**此半句归领班改（Codex 只管 verify.md）**。
2. 八行出处（36 桌清单，领班已核）：唯一入口可长期红（6.11 已治）、出处可自相矛盾（6.12/6.13）、通道可静默失效（6.14/6.19）、禁令守全仍做错（6.15/6.17）、权限面不可自省（6.19）、假绿与真绿同形（报告 §3 末）、结构绿≠判据真、跨平台复现（§3.2 报告）。
3. Codex sandbox 用 `workspace-write`（要写 verify.md）；它不跑验收（我跑）。

## 交什么

1. `verify.md` 末尾新节「## 本套验不了什么（→ harness）」：八行总账，每行＝现象一句＋`todo` 行号回链＋出路一句。
2. 根 `CLAUDE.md`「写报告先读」行加半句转译落点（领班做）。

## 验收命令（bash 用 `D:\Tools\Git\bin\bash.exe`）

| 格 | 命令 | 应当读到 |
|---|---|---|
| 1 | `grep -c '^## 本套验不了什么（→ harness）' docs_meta/src/verify.md` | `1` |
| 2 | 新节内 `grep -oE '6\.[0-9]+[a-z0-9]*' docs_meta/src/verify.md | sort -u | wc -l` | ≥ `6`（行号回链覆盖面） |
| 3 | `git diff --numstat -- docs_meta/src/verify.md` | 纯插入（删除 `0`） |
| 4 | `bash docs_meta/tests/check-sect.sh` | 退出 `0`（根锁落点同步后） |
| 5 | `bash docs_meta/tests/run.sh` | `18 本`；`ALL PASS`；`0` |
| 6 | `git status --porcelain` | ⊆ {verify.md, CLAUDE.md, todo.md, SESSION.md, PROMPT_057.md(新), queue.md} |
| 7 | `grep -c 'cmd/PROMPT_057.md' docs_meta/docs/todo.md` | `1` |

## 不交什么

- 不改八行对应各行本体（总账是收拢不是销案）；不动 `run.sh` 本数；Codex 不 commit。

## 禁令

- Codex 只写 `verify.md` 一个文件（sandbox 保证＋指令点名）；删任何既有内容即断点。
- 总账不许写「已解决」——六条里数条仍是活账。

## 闸一请示

（无。材料齐、判据 grep 形；Codex 试运行人已点名。）
