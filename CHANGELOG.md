## Version binding (unreleased)

- Align host rule checks with fixed product A, development checks with B, and explicit upgrades with candidate P and host state; preserve drift checks and controlled recovery.

## Product checks layout (unreleased)

- Move packaged environment checks from `tests/` to `checks/`; keep development tests at the repository root.

## Factory lifecycle (unreleased)

- Add fixed-product bootstrap and factory install/plan/apply/status/rollback, reusing runtime merge and recovery.
- Distinguish verified ordinary submodules from missing managed runtime records.
- Support product-only release repositories; clarify pinned recovery and explicit upgrades.

<!-- 工作树迁移说明，尚未发布tag。 -->
目录试版：代码移至src/dossier，规则移至docs/rules，模板移至templates，检查移至tests/checks。
统一入口为python dossier.py <command>；旧路径只在对应旧版本可用。next尚未接入稳定自用子模块，7.2发布能力未恢复。

# Changelog

## v0.3.0 — 2026-10-12

**多桌会说话了。**

### 新能力

- **桌间信箱**：多张 Dossier 桌通过 git 私仓互送信件（一桌一地址、领班当邮差、纯文本、可选适配器不装零影响）。装法 `init --with-mail <url> --desk <地址>`，工具 `postman.py`（draft/seal/send/receive/selftest）。
- **回避立法**：卡点名的产品路径对写卡手只读至结案——写卡的手不施工，施工的手不留痕于卡。
- **工牌作用域推广**：凡按卡施工必发工牌（串行只是特例）。
- **印窗指纹机检**：卡落盘→红印之间卡点名路径零变更的机械检查（第 22 本检查）。
- **装桌行为自测**：init 铺完骨架后自动跑两问（语义在＋行为咬），失败大声红。
- **转译基线**：init 落 `.dossier/baseline.json`（逐件 blob-sha1＋时戳＋母本 HEAD），一条命令比对漂移。
- **档案目录**：`docs/archives/` 两层制——todo 只瘦不胖（工作面），案卷只增不删（记录层），随发布归档。

### 门面

- readme v0.3：问题序＋三层披露＋桌间信箱入门＋readme_en.md 中英分立＋「Dossier 的一天」架构图信箱入图＋首屏范式转变插画（精灵消散的聊天窗口→盖章的卷宗）＋三拍「为什么」段。
- 中英两页顶部互链，快事实纪律（无版本锚/价格/战绩）两页同守。

### 基础设施

- push 特许三钉入法：只限邮局仓、专用凭据、母本仓永禁一字不动。
- check-done/check-verdict/check-sync 改扫 todo＋archives 并集。
- 地址簿制：人手写、先到先得、撞名改名才能进。
- 归档机制：发布即归档，当代闭行入档、开新页、todo 重生。

### 已知欠账

- postman submodule 形在真托管上的终验（本机 Git submodule 现场坑，C 层 clone 兜底已实现）。
- 对人推送（微信门铃）为占位，殿后实装。
## v0.2.0 — 2026-10-07

上一版之后的节奏：队列与自动化从「立法位」走到了「实转位」——本仓库自己的硬化批（#34–#44 十一刀，连同值日两刀）就是用它跑的，每刀一报、人只裁断点。

### 这一版有什么

- **队列与代理席**：序列授权一次，代理按式代点行、写卡、派手、审查、结案（蓝印，效力同人印、只标操作者）；七断点永远停呈人；push 对代理永远禁止（`queue.md`＋`roles.md` 代理席节）
- **可盖谓词成命令**：「这一刀能不能结案」收成一条机读查询（`check-verdict.sh`）；无谓词不扩权，连续返工停批的影子门槛 v1
- **模型路由与 Codex 通道**：角色模型下限入条文，`.codex/` 编译目标，Codex CLI 实现席实测（含挂死病理与回落路由）
- **宿主无关层＋起步闸**：`check-env` 新 E 段开工自检执行架构在场性（全无→明记不适用；半身不遂→红）；进 mirror 的配置随子模块旅行，宿主私有件清单点名
- **转译内容戳**：十七源节逐节哈希＋豁免声明形状（`section_stamp.py`＋`check-stamp.sh`，第 21 本检查）；`CHANGELOG` 分「宿主需重译／母本内部」
- **卡面与流程硬化**（硬化批 #34–#44 十一刀）：占位裂行四格、登记与落点五小格、卡外声明行、只读外部树判据、子模块指针句、`.tmp/` 证据升格去处、长文档「存档／工作面」二分、吸收式结案落形、反馈到达即处置
- **自动化建制**：载体与降级阶梯入条文（常设／死账／人点火，不阻塞开发）；值日手与双向巡查（三态回信、信箱、盘上交叉验证）；`duty_probe.py` 心跳 deadman 探针；唤醒回路先例（系统计划任务碰文件＋代理耳朵听）
- **装桌与样例**：`docs/SETUP.md` 五步装桌检查单（`init` 铺出）；`examples/` 冒烟样例；机械检查 18 → 21 本

### 没有什么（未实现，不写「下一阶段」）

- 英文全页翻译
- 全自动排序列队：谓词、载体、值日手已就位，**排哪个序列、何时点火、何时发布仍归人**（照无谓词不扩权与发布明令）
- `docs/reports/` 样例已不再缺：运行时选型、反馈处置、工具特化调研等在案（含外部代研究席交付先例）

## v0.1.0 — 2026-10-02（预估结案日）

一套给 AI 编程代理用的流程约束和 harness 配置，第一个公开发行版。

### 这是什么

Dossier 以 git submodule 挂进你的仓库，`init` 在你的仓库根上铺出 `docs/` 骨架、约定文件和角色文件。此后代理按它的规矩干活：一次一刀、两席两会话、验收判据先行、说「通过」必须指得出能复现的证据。

### 这一版有什么

- 两席 + 两闸 + 卡片的全流程（`docs/rules/workflow.md`）
- 层 × 手的写权限表与目录权威分层（`directory.md` / `roles.md`）
- 骨架生成器：`python dossier/dossier.py init` 铺桌
- 十八本机械把关（`tests/run.sh` 一条入口）
- `templates/` harness 一份（Claude Code 形状），开关两席共用
- 序列与代笔的建制：可盖谓词查询（`check-verdict.sh`）、队列授权（`queue.md`）、代理席与蓝印条款

### 没有什么（未实现，不写「下一阶段」）

- 英文全页翻译
- Codex（`.codex/`）落点
- 自动盖章的全自动队列（谓词与立法已就位，序列仍按刀呈报）
- `docs/reports/` 样例

### 已知的坑

见 `docs/TODO.md` 第 6 章（历史 bug 攒批区），不复述。36 桌的反馈报告（`docs/reports/dossier-feedback-2026-09-17.md`）收录了十二条实测问题及回流情况。

### 刀外落盘记账

- `c1f449b`：text-to-image 的 skill 与命令在刀外提交，其提交文自认 outside the knife commits——记一笔账，不回改（反馈建议 12；2026-10-06 落账，哈希本仓亲核为提交）。
- `workflow.md:270`「换根带走」为 src 残留旧词（换根 2026-09-14 已摒弃，2.8b 判据 src 归零）——既有偏差记档不治，待回流刀（6.22 续块侦察指认，2026-10-06）。
- `4d45ae0`：`design/model-tiers.md`＋`figures/model-tiers.png` 调研稿，刀外提交（空转期调研授权，人 2026-10-02 原话在 `queue.md`；5.26 记账形，2026-10-06 落账）。
- （邻席刀外）：harness-specialization-bet-research-2026-10-07-dsh-glm5.3.md＋figures——独立调研报告，不占刀；写入授权＝人 2026-10-07 原话逐字（存报告头）；由领班按 5.26 记账形代落（该调研席自落未果，文件静默 7 分钟后代提交）。
- （本笔随账）：`tests/check-skel.sh` 骨架计数 36→37——PROMPT_083 裁定 5 的必然机械连带（init 多铺 `docs/SETUP.md` 一件，幂等末行跟着走）；卡面格 7 立格时漏收该件，台账留痕判刀内连带，不松判据（2026-10-06）。

### 重译分拣（宿主需重译）

- 2026-10-06（5.19/PROMPT_082）：17 转译源节取法入法（span/元数据排除/EOL）＋豁免声明形状出生——宿主侧转译需按 `src/tools/section_stamp.py` 现算比对跟进。

### 许可证

MIT。

## Unreleased — explicit runtime upgrades

Added local runtime plan/apply/status/rollback commands. Host execution files and a pinned product submodule can update only after annotated product publication, with three-way customization handling, conflict reporting, finite recovery and guarded rollback. Release reports publication separately from host update failures (exit 3); ordinary unrelated publishing retains its original contract. No production host adoption, tag, commit or push is performed by this development change.

## Development figure tools (unreleased)

- Move figure generators to development `examples/figures/`; keep product images, render stamps, and runtime tools.
