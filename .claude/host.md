# 操作说明，不是开关

下面这几条是宿主怎么用，不是这张桌的规矩，别当判据引。

**动过 `.claude/` 要重载窗口才生效。** 代理名册是会话进程启动时扫一次的快照，之后不重扫。
新加或改名 `.claude/agents/*.md`，当前这个会话看不见，派的时候报
`Agent type 'xxx' not found`。skill 和 settings 同理。

重载窗口（VS Code / Cursor 的 Reload Window）之后名册重建，新的那几只手就派得动了。
`--resume` 同一个会话也重建。2026-09-12 实测过这三格。

**这不是文件坏了。** 撞上的时候先看会话是什么时候起的，别去改 agent 文件。
`2.6c` 那一刀就是这么误判的：会话 09-08 起，`.claude/agents/` 09-12 才落盘，
差了三天半，所以整刀都派不动，当时记成了「这个 harness 派不出任何一只手」。

## 这一份开关两席是怎么读到的（2026-09-12 实测）

实现席：根 CLAUDE.md 里那一行 @ 导入，会展开。
规划席：.cursor/rules/*.mdc 带 alwaysApply: true 的正文自动进上下文；@ 导入行一律不展开。

这两格是外部产品那一天的行为，不是常量。换一组平台要重走一遍这个编译流程，
一组平台走一次。厂商改了机制，这份产物会静默失准，盘上不会红——这是明着留的残余。

## Bash 弹窗：A 档前缀（2026-09-13）

不是这张桌的规矩，不当判据引。人裁：A 直接改项目 `.claude/settings.json`，B/C 暂不处理。
读测前缀：`grep` / `sed -n` / `echo` / `wc` / `head` / `tail` / `mkdir`、`bash docs_meta/tests/*`、只读 `git status|diff|log|ls-files`。
假根 `SWITCH_ROOT=` / `SECT_ROOT=` 以及换成 `env SWITCH_ROOT=* bash docs_meta/tests/*` 都量死了，不放。
不写 `Bash(env *)`（罩住 `env` 能起的任何进程）。假根跑 `check-switch.sh` / `check-sect.sh` 接受每次弹一下。
**没放** `tee`、`chmod`、`awk`。改完要重载窗口。

**没验过的一句，写在改动旁边：** 前缀够宽之后，宿主还往不往 `settings.local.json` 追加原文，本席没量。
A 本身是写权限：`echo … > 文件`、`grep … > 文件` 实测静默且真落盘，不是「只读旁边有洞」。
路径形 `deny` 拦不住 `>`（参数位拦、重定向位不拦，已量）。堵它只剩 hook，人裁只记不修。

人 2026-09-13 后裁：git 写操作堵严，其余不管。项目 `settings.json` 的 `deny` 拦
`git commit` / `push` / `reset` / `rebase` / `checkout` / `switch` / `clean` / `restore` / `stash`（含 `git -C …` 那一形）。
`status` / `diff` / `log` / `ls-files` 仍在 allow。`&&` 拼在后面的写操作前缀匹配可能罩不住，厂商文档如此，不吹。改完重载窗口。

人又裁：壳上动 `.git` 目录也盖大面（拦君子不拦小人）。`deny` 加 ` .git` / ` .git/` / `/.git/`、`GIT_DIR=`、`--git-dir=`。
不写 `*.git*`，以免误伤 `.gitignore`。Edit / `python -c` 仍绕得过，不补。`.git/` 连只读也拦，是既定代价。

死规则已从 allow 删掉：`Bash(py -3 -c ' *)`、`Bash(awk *)`、`Bash(SWITCH_ROOT=*)`、`Bash(SECT_ROOT=*)`、
`Bash(env SWITCH_ROOT=* bash docs_meta/tests/*)`、`Bash(env SECT_ROOT=* bash docs_meta/tests/*)`。
进库那一份里画图标 / 本机 Edge 的 10 条精确原文也清了，换根不再带走。
一次性路径探针 `Bash(* d:/tmp/perm_probe_deny.txt)` 量完已删。
