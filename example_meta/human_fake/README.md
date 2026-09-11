# 假人（v0）

读领班收口，吐两行，交给领班。不写卡。

```text
判断：是
理由：
```

两种模式：

| 模式 | 做什么 |
|---|---|
| `dumb` | 不打模型，只会 `判断：是`，理由空。默认。 |
| `reason` | 打模型，做基本判断，理由写一句。没配密钥则仍回落到 `是`。 |

```text
python human_fake.py sample_report.md
python human_fake.py --mode reason sample_report.md
```

`.env` 里 `FAKE_HUMAN_MODE` 也能切；命令行优先。
`.env` 不入库。reason 档的提示词在 `prompt.md`。
