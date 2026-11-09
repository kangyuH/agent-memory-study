# 使用 Agent Memory 研究 Skill

在仓库根目录打开 Codex，按期数调用 Skill。

```text
用 $agent-memory-research 研究 EP01，信息截止日用今天，输出到 outputs/agent-memory。
先设计研究问题，核对一手资料、相反证据和适用条件。完成独立审核后导出研究资料。
```

可为单期设计问题和检索计划，恢复中断，核查资料，或按显式依赖批量处理。换课程时传入新的 `outline_path`，采用 `## 主题` 与 `### EP01｜标题`。把必须满足的研究依赖写在 `## 跨章节知识依赖` 下，例如 `- EP01 → EP02`。

## 运行条件

- 使用可运行 Python 3.10+ 的 Codex Unix 工作区，并准备可写的输出目录。
- 使用可打开一手原文的工具，以及独立审核会话或人工审核者。
- 使用用户时区日期作为默认研究截止日。历史论文和现行实现分别记录实际版本。
- 默认 `deep` 扩展问题维度、证据版本与反证。`focused` 可收紧可选探索，必要问题使用同样的验收要求。

[模式、参数与恢复命令](../.agents/skills/agent-memory-research/references/operations.md)

## 输出与验收

`course/<大纲哈希>/course_index.json` 保存大纲索引。`runs/<期数>/<运行 ID>/` 保存检查点，`releases/<版本>/` 保存导出。

| 资料 | 用途 |
| --- | --- |
| `research_questions.json`、`coverage.json` | 问题清单、证据映射及研究缺口 |
| `research.md` | 主要研究资料，按问题归纳证据和限制 |
| `references.md`、`evidence_matrix.md` | 完整的一手来源索引与主张追溯 |
| `technical_notes.md`、`concepts.json` | 机制细节、术语和跨期一致性记录 |
| `review_research.md`、`review_final.md`、`acceptance_report.md` | 独立核验、终审与验收 |
| `manifest.json` | 输入版本、覆盖统计、审核记录和产物哈希 |

使用 NotebookLM 时可以先导入 `research.md`，再按需加入证据矩阵、技术笔记与原文。听众解释、讲述顺序和例子由下游选择。

必要问题缺少证据时查看状态中的缺口和补证动作，保留已核验材料，从有效检查点恢复。自动检查验证问题与账本的映射、缺口、产物完整性和快照。独立审核负责确认来源真实性、证据含义与覆盖充分性。历史试跑包可按原清单查询和导出。

[验证记录](skill-validation.md)

```sh
python3 -m unittest discover -s tests -v
```
