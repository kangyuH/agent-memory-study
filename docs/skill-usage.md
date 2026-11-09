# 使用 Agent Memory 研究 Skill

在仓库根目录打开 Codex，按期数调用 Skill。

```text
用 $agent-memory-research 研究 EP01，信息截止日用今天，输出到 outputs/agent-memory。
先核对一手资料，完成两次独立审核，审核通过后导出 NotebookLM 资料包。
```

适用场景还包括先为单期出研究计划、恢复已有运行、单独审查稿件，以及按依赖顺序处理主题或期数范围。换课程时传入新的 `outline_path`，采用 `## 主题` 与 `### EP01｜标题` 的结构。需要严格排序的依赖写在独立的 `## 跨章节知识依赖` 下，例如 `- EP01 → EP02`。

## 运行条件

- Codex 能读取仓库 Skill，并可运行 Python 3.10+。检查点脚本使用 Unix 文件锁。
- 有可以打开一手原文的工具、独立审核会话或人工审核者、可写的运行目录。
- 使用当前用户时区的日期作为默认研究截止日。历史材料和较新的实现按各自实际版本记录。
- `deep` 为默认深度。验证少量核心机制时可用 `focused`，审核硬门槛保持一致。

[模式、参数与恢复命令](../.agents/skills/agent-memory-research/references/operations.md)

## 输出与验收

`course/<大纲哈希>/course_index.json` 保存大纲索引。各期的工作与检查点在 `runs/<期数>/<运行 ID>/`。发布包在该运行的 `releases/<版本>/`。

| 资料 | 用途 |
| --- | --- |
| `podcast_source.md` | NotebookLM 主输入 |
| `notebooklm_source_list.md` | 一至四份关键一手来源及各自用途 |
| `research.md` | 完整研究母稿 |
| `references.md`、`evidence_matrix.md` | 来源与主张追溯 |
| `review_research.md`、`review_final.md`、`acceptance_report.md` | 两次审核与最终验收 |
| `manifest.json` | 输入版本、阶段或发布状态、审核记录和文件哈希 |

缺少关键原文、审核者或其他必要能力时，读取状态中的阻塞原因与修复动作。完成补证后使用原运行恢复。内容修订后回退至仍有效的检查点，重新验证受影响的下游稿件。输出目录可包含本地路径和运行记录，分享时选择所需资料。

自动检查覆盖格式、引用编号、可追溯性和状态。来源真伪、技术含义、实验可比性与结论边界由独立审核确认。审核分数档位先按试行值运行，结合后续验收结果校准。

[验证记录](skill-validation.md)

```sh
python3 -m unittest discover -s tests -v
```
