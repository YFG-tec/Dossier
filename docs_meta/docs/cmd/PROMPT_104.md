# PROMPT_104 · 5.49 首屏范式转变插画——聊天会蒸发，卷宗长存

| | |
|---|---|
| **本刀是 TODO 哪一行** | `todo.md` `5.49`（人 2026-10-11 原话在行内） |
| **状态** | 第 1 版（人「先用这个」即点火；微刀，卡文与红印同轮落） |
| **落槌来源** | 人 2026-10-11「我看到了，先用这个，附加点儿文字说明，我们准备提V0.3了」＋十二轮生成迭代全记录在 `.tmp/hero-draft/` |
| **前置，满足了** | hero-v11-clean2.png 定稿（1536×678，无字无水印，image-reader 亲验「无文字无数字」）；readme/readme_en 现文亲读（5.48 刚结） |
| **档位** | 重（门面件）。微刀不改档位值 |
| **谁来建造** | 独立 subagent（工牌制） |
| **独立审查** | 读者手一顺位（图注与图义合不合）；事实手二顺位（alt 实况、互链不破、快事实零、AI 声明在） |
| **写到哪几处** | ①`docs_meta/src/figures/paradigm-shift.png`（新，拷贝自定稿）②`readme.md` ③`readme_en.md` ④记录件 |

## 裁定（卡上定死）

1. **图件**：`hero-v11-clean2.png` → `docs_meta/src/figures/paradigm-shift.png` 原样入库，不再加工。
2. **中文页**：口号块下方居中插图 `width=560`；图注一行（小字、居中）：「聊天气泡里的对勾会蒸发；卷宗里盖了章的对勾，立得住。」；alt：完整描述三元素（碎裂消散的聊天窗＋粒子流、箭头、摊开账本上的红对勾与爪印）。
3. **英文页**：同位同宽；图注："A checkmark in a chat bubble evaporates; one stamped into a case file stands."；alt 英文对应。
4. **AI 声明**：两页文末「那枚爪印」节各加一行——中文「首屏插画：GLM-Image 生成，人工修裁。」／英文 "Hero illustration: generated with GLM-Image, cropped and cleaned by hand."
5. **不越界**：不动首屏其余元素（互链/图标/h1/口号/head note 原样）；不动架构图；不动 22 本检查；图内不加任何文字。
6. **记录件**：todo 5.49 挂卡指针；SESSION 覆盖；queue #62 在办。

## 验收命令（日志树外）

| 格 | 命令 | 应当 |
|---|---|---|
| 1 | run.sh（树外） | 22 本 ALL PASS（结案时） |
| 2 | `rg -c "paradigm-shift" readme.md readme_en.md` | 各 ≥1 |
| 3 | `rg -n "GLM-Image" readme.md readme_en.md` | 各恰 1 |
| 4 | 图注两句逐字在两页 | 命中 |
| 5 | `git status --porcelain` | ⊆ 本卡点名处 |

## 不交什么

- 不动架构图/首屏其余/检查口径；不重制图；不发 tag（发布另刀归人）。

## 禁令

- 图内零文字；快事实零；两稿图注义合；朱红语义不破（印章＝核验）。

## 闸一请示

（无。图与图注均系人本轮原话定向；AI 声明系去水印后的诚实对价。）
