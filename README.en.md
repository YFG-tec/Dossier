<p align="center">
  <img src="docs_meta/src/figures/dossier-icon.png" width="168" alt="Dossier: one folder drawn from a stack, labeled on the spine, closed only by a paw seal">
</p>

<h1 align="center">Dossier</h1>

<p align="center">
  <b>One cut at a time; nothing counts until it is stamped.</b>
</p>

<p align="center"><i>中文版见 <a href="readme.md">readme.md</a>。</i></p>

---

**Dossier is a set of process constraints and harness configuration for AI coding agents.** Mount it into your repository as a git submodule, run `init` once, and it lays down a `docs/` skeleton, `CLAUDE.md` / `AGENTS.md`, and a few role files at your repo root. From then on the agent works by its rules: one card's worth of work at a time; writing the card and writing the code happen in two separate sessions; acceptance criteria are declared before anything runs; saying "passed" must point at reproducible evidence.

**Who it's for**: work where green tests do not mean correct — numerical solvers, data pipelines, anything whose deliverable is *a claim* rather than *a running thing*.
**Who it's not for**: projects whose failures are loud. Compile errors, blank pages, users noticing on the spot — there, this density is a tax, not insurance.

```text
your-repo/
  CLAUDE.md  AGENTS.md        conventions the agent reads before each work item
  .claude/   .cursor/         role files, switches
  docs/
    TODO.md  SESSION.md       backlog; the running state of the current cut
    cmd/  design/  reports/   per-cut cards; the contract layer; stage deliverables
  dossier/                    the submodule. The source of truth itself — you don't edit it
```

Install in two steps:

```text
git submodule add https://github.com/YFG-tec/Dossier dossier
python dossier/docs_meta/src/init.py
```

Read on for the details; if you just want to install, those two lines are enough.

## The Stack of Files

A stack of case folders; one is drawn out at a time and worked on. A label on the spine tells you which one it is without opening it. When the work is done it gets a stamp — nothing counts until stamped, and the stamp is never pressed by the hand that did the work. Draw one out, and the stack remains.

The project's English name is `Dossier` — a case file. The Chinese name, 绘卷, means a hand scroll: both are about bound records. A case file is a bundle you can identify from the spine without opening; a scroll is the whole stack laid out for you to see.

| Word | What it refers to |
|---|---|
| **Dossier** | This repository. The discipline itself |
| **Desk** | A project repository that runs on it |
| **Cut** | One unit of work at a desk |

**There is exactly one source of truth, and desks are cut from it one by one.**

This system was distilled out of several numerical projects built along the way. Each desk kept its own implementation and exploration path. Dossier is not a compilation — it is **extraction, unification, abstraction, and upgrading**: gaps a single desk never noticed get filled; redundancies that get in the way of management get dropped. What one desk has does not automatically enter the common layer, and old desks are under no obligation to backport. See `docs_meta/src/sources.md` for the mapping.

---

## Why It Holds

The axis for choosing a management weight is whether the criteria are exogenous or endogenous — not project size. With exogenous criteria (a reference implementation, a gold standard), go long-running with sparse supervision; with endogenous criteria (you are constructing the truth yourself), go short cuts with dense gates. In the first regime this system is a tax; in the second it is the thing itself.

The second axis is whether failures are loud. A compile error or a mismatch against reference output is loud; silent numerical degradation — an enum that declares three modes, a kernel quietly used as the default, contract tests all green — is not. **What dense gates buy is not speed; it is making silent failure surface within a single cut.** This argument can never be "the model isn't good enough yet"; it can only rest on those two legs — endogenous criteria and silent failure. The day those two no longer hold, the right move is to retreat to long runs, not to add rules.

A human project could not afford this management density. It holds here because **the marginal cost of following rules has dropped to nearly zero**: writing cards, writing state to disk, auditing item by item — for an agent this is trivial, and documents are its only stable memory. The rules are detailed not because anyone is clever, but because we can finally afford it.

Criteria declared up front, evidence that can be replayed, and the stamping hand is never the working hand. The core is not conversion — it is credibility: not turning raw material into product, but making a conclusion **believable**.

Deviations must each state their cost in writing; a hidden deviation is itself a class of failure. Outstanding debts are laid out in `docs_meta/docs/todo.md`, chapters 5 and 6. How this was built — next section.

---

## The Frame

The skeleton has five beams: **two seats, two gates, the card, layered authority, and state on disk.**

Three more hang off those beams: dedicated hands and independently re-run evidence hang off "two seats"; append-only records hang off "state on disk"; the one-way source → artifact direction hangs off "layered authority" — artifacts are only ever compiled from source; to change behavior you change the source end. Disagreement between the two is not the criterion; the direction is.

**The two seats** are not two AIs writing code together. The division is differences in capability plus differences in permission. Which harness sits in which seat can change; **that the two seats are two separate sessions cannot**. A role is not a persona — it is **write permissions + what it may do when things fail**.

- The hand that writes the card does not go on to edit the core
- The hand that edits the core does not touch test criteria
- The hand that writes tests does not fix the core to green
- The review hand writes nothing; it only checks results against pre-declared standards
- The planning seat saying "continue" cannot open `src/`

**The two gates**: one to open a cut, one to close it. The human stands only at those two gates.

**The card** is the sole permit surface of a cut. One cut, one card; without a card, the core is untouchable.

**Layered authority**: the sources are the normative text; everything at the root is compiled harness.

**State on disk**: state is recorded under version control, reproducible, and never drifts inside a chat.

What it guards against — seven classes of failure:

1. **Overselling.** You ask for one line of verification; it opens the next phase on its own.
2. **State living in chat.** Switch windows, scope drifts.
3. **Planning and implementation wrestling over the same core.**
4. **Probes that can't be replayed.** A report cites `.tmp/run_*.py`; the deliverable rots the next day.
5. **Tests that cannot fail.** Expected and computed values share one source.
6. **Loosening a knob when things scatter.** The symptom disappears; the contract was swapped.
7. **Charts nobody looks at.** The real error only shows when the picture is opened.

**Separate authority by directory first, then lock scope with one cut. Scope, contracts, evidence, and permits all land on disk.**

<p align="center">
  <img src="docs_meta/src/figures/dossier-frame.png" width="880" alt="Authority as directory layout: a matrix of seven columns and five rows. Columns are the seven layers — conventions, contracts, in-progress, implementation, gatekeeping, delivery, drafts; rows are the human, the planning seat (Cursor by default), and the three hands inside the implementation seat — builder, tester, reviewer — the last three bracketed into one seat (Claude Code by default). Three marks fill the cells: a solid square for write, a hollow circle for read-only, a dot for untouchable. In the human row, the in-progress cell is vermilion — the only color in the whole figure, because only the human can set it. In the contracts column, human and planning seat are solid while the implementation hand is a hollow circle with an asterisk, noted that a card must name it before contracts change; the implementation and gatekeeping layers each belong to one hand; the review row has no solid square at all, captioned below that the review hand writes nothing. Under the table a light gray band titled 'changing phase is changing hands' lays the same hands on a timeline: the planning seat opens the case, the implementation seat's three hands walk build, evidence, and audit in sequence, the human closes it; two dashed gates mark 'do it by the card' and 'tick the TODO'.">
</p>

Installing is two moves: mount the source of truth as a submodule, then run `init` once.

```text
1. git submodule add https://github.com/YFG-tec/Dossier dossier
2. python dossier/docs_meta/src/init.py
```

Name the submodule directory whatever you like; `init` computes paths from its own location. It lays files one level above the submodule — at your repository root. What it lays down is an empty shell, not a sample: the directories and drop points are there; the content is yours to write. The harness files at the root are copied from the source's `.mirror/`.

Re-running only fills in what's missing and never overwrites what exists, so upgrading is the same road: `git submodule update --remote` to pull the new version, then run `init` again. The boundary is physical — inside the submodule directory belongs to the source of truth; outside it, everything belongs to your desk.

Open the details as needed; no need to read them all first:

| What you want | Read |
|---|---|
| Directory layout, where figures go | `docs_meta/src/directory.md` |
| One cut, cards, closing audit | `docs_meta/src/workflow.md` |
| Verification, troubleshooting | `docs_meta/src/verify.md` |
| Roles, weight settings | `docs_meta/src/roles.md` |
| Landing on Claude Code | `docs_meta/src/claude-code.md` |
| Landing on Cursor | `docs_meta/src/cursor.md` |
| What's out there, why not that way | `docs_meta/src/sources.md` |
| Open questions | `docs_meta/docs/design/open.md` |

---

## The Paw Print

Humans lost the race with large models on writing code long ago; but the final mark that lands — that is the soul.
