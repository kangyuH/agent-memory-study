# 研究计划模板

## episode_brief.md

- 本期议题和适用范围。
- 需要核查的定义、术语与背景版本。
- 直接证据依赖、相邻范围及排除理由。

`scope_contract.json` 使用 `episode`、`include`、`related_context`、`exclude`、`prerequisites`。后四项是字符串列表，前置期编号按 `scope_input.json` 的顺序填写。

## research_plan.md

- 问题清单与检索方向，标明搜索语言、来源类型、时间或代码版本和停止条件。
- 对照可检索问题检查定义与概念、历史与版本、机制、替代路线、实证、反例、限制及开放问题。无关维度说明原因。
- 记录待验证的相反结论、遗漏风险及原文不可达时的替代来源。

`research_questions.json` 是对象列表。每条有 `question_id`（如 `Q01`）、`question`、`basis`（为何纳入范围）与布尔值 `required`。至少一个问题为必要项。必要项用于识别足以影响本期结论的缺口，保留能改变结论的反证。
