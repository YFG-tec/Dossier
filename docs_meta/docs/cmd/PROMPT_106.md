# PROMPT_106 · 5.51 首屏三拍第一拍——锚定代码场景＋一面之词

| | |
|---|---|
| **本刀是 TODO 哪一行** | `todo.md` `5.51`（人 2026-10-12 两轮原话在行内） |
| **状态** | 第 1 版（含人 2026-10-12 三轮修订，闸一之后动过的见下节） |
| **落槌来源** | 人 2026-10-12「AI说'做完了'，有没有更好的表达」「AI有点太宽了，我们仅指vibe coding这一个场景」＋「可以」 |
| **前置，满足了** | 5.50 刚结（三拍在位 :19）；两页现文亲读 |
| **档位** | 重（门面件）。微刀不改档位值 |
| **谁来建造** | 独立 subagent（工牌制） |
| **独立审查** | 读者手＋事实手（快审） |
| **写到哪几处** | ①`readme.md` ②`readme_en.md` ③记录件 |

## 裁定（卡上定死）

1. **中文第一拍**替换：将 `AI 说「做完了」，你无法验证；窗口关闭，过程随之消失。` 替换为 `窗口关闭，过程随之消失——设计取舍、验证经过、开发轨迹，皆不可查。`
2. **英文第一拍**替换：将 `When the agent says "done," you cannot verify it — and once the window closes, even the process is gone.` 替换为 `Close the window, and the process is gone — design decisions, verification history, the paths tried and abandoned, all beyond reach.`
3. **不动**：第三拍、图注、首屏其余一切、图、检查。`n4. **BOM 修复**：两页行首 UTF-8 BOM 剥去（事实手 MUST-FIX，读数在案）。

## 验收

| 格 | 命令 | 应当 |
|---|---|---|
| 1 | run.sh | 22 本 ALL PASS |
| 2 | `rg -c "一面之词" readme.md` | 1 |
| 3 | `rg -c "agent's word" readme_en.md` | 1 |
| 4 | `rg -c "做完了，你无法验证" readme.md readme_en.md` | 0 |
| 5 | `git status --porcelain` | ⊆ 两页＋记录件 |

## 闸一请示

（无。措辞经人两轮裁定逐字入卡。）
