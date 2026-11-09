# 独立审核与验收

在与写作者分开的上下文中审核。可以使用独立审查代理、单独会话或人工复核。交付原始来源、范围契约、当前快照和本页门槛，省去写作者的自评与结论提示。审核者自行重开原文、逐条核实所有核心主张，并反向抽查稿件中其他事实，按需复现关键机制。母稿审核与最终审核使用不同会话。缺少实际独立审核时记录阻塞。脚本核验身份和快照记录，不能代替独立审查的执行。

审核事实与来源、技术机制、证据强度与反例、年代和版本、课程边界与跨期一致性、工程价值与失效场景。专查来源身份伪造、引用与结论不符、时间倒灌、实验不可比、算法错解、无条件优越性、推断冒充事实、缺失反证和抢讲重复。最终审核额外检查音频稿有无新增主张、实验或例子，并检查资料包完整性。

| 字段 | 分值上限 |
| --- | --- |
| `facts` | 30 |
| `mechanisms` | 25 |
| `tradeoffs` | 20 |
| `scope` | 10 |
| `audio` | 10 |
| `traceability` | 5 |

母稿审核的 `audio` 维度衡量能否从母稿提取有边界、可口播且证据充分的材料。最终审核以实际资料稿评分。试行档位 `standard-v1` 为 85 分，`strict-v1` 为 92 分。记录人工抽查结果再定标。硬性门槛独立于总分。

## 审核文件

每次保存 Markdown 审核报告和 JSON，分别命名 `review_research.md` / `review_research.json` 或 `review_final.md` / `review_final.json`。

- JSON 含 `episode`、`reviewer_id`、`review_session`、`review_method`（`independent_agent`、`independent_session`、`human`）、`verdict`。只有真实通过才用 `pass`。
- 把启动审查时 `status` 输出的 `reviewed_sha256` 原样带入审核记录，重新取证后仍核对实际快照。记录已复核主张编号 `verified_claims`。附上述六项整数分 `scores`。
- `hard_gates` 的键为 `sources`、`mechanisms`、`traceability`、`chronology`、`failure_modes`、`comparison`、`scope`、`cross_episode`。最终审核增加 `audio_consistency` 与 `package`。全部为真才可通过。
- `issues` 为对象列表，每项包含 `issue_id`（`I01`）、`severity`（`BLOCKER`、`MAJOR`、`MINOR`）、`status`（`open`、`fixed`、`accepted`）、`location`、`evidence`、`fix`、`verification`。批准暂缓的重大问题须写 `rationale`。阻塞项须修复并复核。保留未通过审核报告，带入修订后的同一问题编号以便追溯。
- `acceptance_report.md` 记录期数、审核快照、关键来源抽查、硬门槛、两轮审核结论、遗留问题与实际导出路径或版本标识。确认通过后再运行发布。
