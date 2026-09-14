# 实现席 Bash 弹窗

**权威：参考。** 全文不带标记，**一条都不可引**。记的是项目 `.claude/settings.json` 里已经落下的权限面，以及量过的宿主行为。
现行表以那一份为准；本页只说明它为什么长这样。`.claude/host.md` 是给操作看的短注，不当判据引。

改的是 Claude Code 问不问 Yes/No，不是这张桌的规矩。前缀怎么匹配是厂商的。本篇不占 `todo.md` 一行：权限表在 `docs_meta/src/` 里没有出处，十四本也验不了它绿不绿。

人 2026-09-13 裁：A 直接改项目那一份；B / C 里除 git 墙以外暂不处理。后面几轮补的是领域（建目录、跑脚本、`chmod +x`），不是把 B 整档打开。

## 1 现态

弹窗几乎全是 **Bash 整句精确匹配失败**。`acceptEdits` 下改文件本身不弹。模型换一行 `grep` / `echo`，再弹一次；人点 Yes，`settings.local.json` 多一条原文。白名单越长，越对不上下一条。前缀 allow 是为了停这个循环。

项目 `.claude/settings.json` 现在分两栏。

**allow（少问）**

| 类 | 前缀 |
|---|---|
| 读测 | `grep *`、`sed -n *`、`echo *`、`wc *`、`head *`、`tail *` |
| 只读 git | `git status *`、`git diff *`、`git log *`、`git ls-files *` |
| 建目录 | `mkdir *`；另有 `.tmp/`、`docs_meta/`（含 `src/` `tests/`）、根上 `src/` `tests/` 的 `mkdir` / `mkdir -p` |
| 跑脚本 | `bash docs_meta/*`、`bash docs_meta/tests/*`、`bash .tmp/*`、`bash src/*`、`bash tests/*` |
| 模式位 | `chmod +x` 到 `docs_meta/`（含 `tests/`）、`.tmp/`、根上 `src/` `tests/`。不放全域 `chmod` |

这张桌是元项目。核和把关住在 `docs_meta/src/`、`docs_meta/tests/`；铺到宿主上之后普通桌用根上 `src/`、`tests/`，两边都放。`.tmp/` 在仓库根上，不是 `docs_meta/` 的子层。

**deny（硬拦，连提示都不弹）**

- git 写：`commit` / `push` / `reset` / `rebase` / `checkout` / `switch` / `clean` / `restore` / `stash`，各带无参、`*`、`git -C * …`
- 壳上碰 `.git`：` .git`、` .git/`、`/.git/`、`GIT_DIR=`、`--git-dir=`。不写 `*.git*`，以免误伤 `.gitignore`

`status` / `diff` / `log` / `ls-files` 在 allow。`stash list` 这种只读子命令也被 `git stash *` 罩住，是既定代价。

**没放**

`cp` / `mv` / `rm` / `tee` / `awk`。人裁 B 停在这；前缀也写不出「只写到自己的目录」。
假根 `SWITCH_ROOT=` / `SECT_ROOT=`，以及 `env SWITCH_ROOT=* bash docs_meta/tests/*`，都量死了，不放。不写 `Bash(env *)`（罩住 `env` 能起的任何进程）。假根跑 `check-switch.sh` / `check-sect.sh` 接受每次弹一下。

网络、`rm -rf`、`python -c` 没拦。Edit / `python -c` 仍绕得过 `.git` 那几条，不补。

进库那一份里画图标、本机 Edge 的精确原文已清，不会跟着铺到宿主上。死规则（`py -3 -c ' *`、`awk *`、假根那几形）已从 allow 删掉。一次性路径探针量完已删。

`settings.local.json` 那堆原文这轮没清，不当第二真相。改完要重载窗口。

## 2 量过的机制

不是读文档推的。厂商改了会静默失准，盘上不会红。

**前缀匹开头。** `Bash(echo *)` 罩得住 `echo x > 任意路径`。重定向不让命令脱出前缀。A 档动词加 `>` 就是写权限，写得到 `SESSION.md` 和卡。不是「只读旁边有个洞」。

**路径形 deny 拦不住 `>`。** 同一条规则、同一个路径：在参数位拦得住，在重定向位拦不住。要堵「A 档动词 + `>`」，`deny` 走不通，只剩 hook。人裁只记不修。

**复合命令按段判。** `;` 和 `|` 拆开的每一段各自过 allow / deny。拿一条允许的命令开头、后面接一条被拦的，塞不进去。每一段里的 `> 路径` 仍被剥掉，不参与判断。

**死规则读不出来，只能撞。** 配置里写着和活规则一模一样，可能一次都没生效：`awk *`、`py -3 -c ' *`、`SWITCH_ROOT=*`、`SECT_ROOT=*`、`env SWITCH_ROOT=* bash docs_meta/tests/*` 都是。加完不撞一次等于没加。

**追加进 local 的字面只有触发的那一段**，不是完整命令。别拿它当当时跑过的全文。

**`deny` 压得住 `allow`，拦在执行之前。** 实现席跑 `git commit` 当场 denied。条款层写着人点「结案」就落笔；落笔那只手不在实现席这边。

## 3 和把关层错开

第十三本 `check-switch.sh` 扫进库的 `.claude/`，项目 `settings.json` 在射程里。宿主会把批准过的 Bash 原文追加进配置。那是检查假红，不是本页要停的弹窗。两件活，不要焊成一行。

## 4 没做的

- B 整档（`.tmp/` 上免问 `cp` / `mv` / `rm`）没开。
- 用 hook 堵 `>` 没开。
- 假根免问没做成。
- 用户级 `~/.claude/settings.json` 不混进本仓这一份。
