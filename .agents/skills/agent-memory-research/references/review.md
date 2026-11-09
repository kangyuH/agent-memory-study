# 独立核验与交付验收

使用与资料整理者分开的上下文，由独立代理、独立会话或人工审核。最终审核与第一次审核使用不同会话。给审核者原文、范围契约、问题清单、覆盖表与当前快照。审核者重开来源，独立判断问题覆盖和证据保真。

- 先核对清单与大纲，主动找遗漏的概念、路线、反例、版本、可比条件和失效模式。逐题查看证据的指向和覆盖状态，判断是否有把必要问题当可选项的情况。
- 核对原文与关键主张的含义、事实与推断的边界、实验的模型、数据、版本、基线、指标、结果、显著性与适用条件。检验未报告内容和检索缺口是否有依据。
- 查看跨期术语、年代与事实冲突。终审复查修订闭合、来源链接、交付文件与对应快照。

| 评分字段 | 上限 |
| --- | --- |
| `facts` | 30 |
| `coverage` | 30 |
| `mechanisms` | 15 |
| `conditions` | 15 |
| `traceability` | 10 |

`standard-v2` 门槛为 85 分，`strict-v2` 为 92 分。必要问题缺口和硬门槛独立于总分。机器检查编号与快照，审核者负责来源真实性、语义对应、问题设计和事实完整性。

## 审核文件

每次保存 Markdown 报告与 JSON，命名 `review_research.md` / `review_research.json` 或 `review_final.md` / `review_final.json`。

- JSON 含 `episode`、`reviewer_id`、`review_session`、`review_method`（`independent_agent`、`independent_session`、`human`）、`verdict`。通过写 `pass`。
- 使用 `status` 返回的 `reviewed_sha256` 绑定快照。以 `verified_claims` 列出复核的主张编号，覆盖所有核心主张。用 `reviewed_questions` 逐一列出审查过的 `Qnn`，报告记录每题的证据、条件或缺口。
- `hard_gates` 为 `sources`、`mechanisms`、`traceability`、`chronology`、`failure_modes`、`comparison`、`scope`、`cross_episode`、`coverage`、`conditions`，终审增加 `package`。全部为真才通过。
- `issues` 是对象列表，每项含 `issue_id`、`severity`（`BLOCKER`、`MAJOR`、`MINOR`）、`status`（`open`、`fixed`、`accepted`）、`location`、`evidence`、`fix`、`verification`。接受暂缓项须写 `rationale`。阻塞项须修复并复核。保留问题编号与历次报告。
- `acceptance_report.md` 记录两轮审核、来源抽查、问题覆盖、可接受的剩余缺口与导出清单位置。
