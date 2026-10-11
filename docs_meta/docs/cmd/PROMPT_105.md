# PROMPT_105 · 5.50 首屏「为什么」三拍——凝练版

| | |
|---|---|
| **本刀是 TODO 哪一行** | `todo.md` `5.50`（人 2026-10-11 三轮原话在行内） |
| **状态** | 第 1 版（人「开吗」即点火；微刀，卡文与红印同轮落） |
| **落槌来源** | 人 2026-10-11「我觉得，为什么这个要简明扼要」「后面再补一句，这么做主要的目的是使得长程项目变得有迹可循，可以容易驾驭」「中文部分的表述在凝练一些，少一些口语化要素」 |
| **前置，满足了** | 5.49 刚结（图在位）；两页现文亲读；图注/正文草稿经人三轮裁定 |
| **档位** | 重（门面件）。微刀不改档位值 |
| **谁来建造** | 独立 subagent（工牌制） |
| **独立审查** | 读者手＋事实手（快审） |
| **写到哪几处** | ①`readme.md` ②`readme_en.md` ③记录件 |

## 裁定（卡上定死）

1. **中文三拍**（图注下方，紧跟 5.49 插画的图注行，作为正文段落）：

```
AI 说「做完了」，你无法验证；窗口关闭，过程随之消失。Dossier 将其变为可验证：每步有记录，每项结论有证据，是否完成，可自行查证。单次脚本无需如此；长程项目由此有迹可循——数周演进、数十轮变更，皆可追溯、可审计，因而可驾驭。
```

2. **英文三拍**：

```
When the agent says "done," you cannot verify it — and once the window closes, even the process is gone. Dossier makes it verifiable: every step leaves a record, every conclusion leaves evidence — whether it is done is something you can check yourself. A one-off script needs none of this; long-running projects become traceable — weeks of evolution, dozens of changes, all auditable, all steerable.
```

3. **图注换词**（5.49 图注句替换）：中文「聊天里的『做完了』会蒸发；卷宗里盖了章的『做完了』，立得住。」→ 不变（已在上轮定稿）。英文 "Done" in a chat evaporates; "done" stamped in a case file stands. → 不变。

4. **不越界**：不动首屏其余（互链/图标/h1/口号/head note）；不动图；不动 22 本检查。

## 验收（日志树外）

| 格 | 命令 | 应当 |
|---|---|---|
| 1 | run.sh | 22 本 ALL PASS |
| 2 | 三拍逐字在两页 | 命中 |
| 3 | `rg -c "无法验证|有迹可循" readme.md` | ≥2 |
| 4 | `git status --porcelain` | ⊆ 两页＋记录件 |

## 闸一请示

（无。三拍措辞经人三轮裁定逐字入卡。）
