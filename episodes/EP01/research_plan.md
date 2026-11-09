# EP01 检索与取证计划

大纲范围见 `episode_brief.md` 和 `scope_contract.json`。冻结问题见 `research_questions.json`。本次截止日为 2026-11-09。下面的论文主题、基准名和检索式用于找一手材料，需在取证阶段核验。

## 问题与查询方向

| 问题 | 维度 | 首轮英文检索式 | 一手证据与期望定位 |
| --- | --- | --- | --- |
| [Q01] | 历史与版本 | `early task oriented spoken dialogue airline travel information slot frame dialogue manager ATIS DARPA`；`dialogue state tracking challenge history rule based statistical neural tracker` | 原始系统说明、项目任务定义、共享任务总览和参赛论文。分开记录任务公开、论文发表、数据与代码版本。覆盖代表性实例并说明取样边界，避免把先后顺序当成替代关系。 |
| [Q02] | 定义与概念关系 | `task oriented dialogue intent slot filling dialogue state tracking policy input output user goal`；`dialogue state tracking benchmark user goal constraints requested slots` | 原论文的系统架构、任务协议和标注指南。比对用户语义、状态假设与动作如何表示，确定可判定每类失败的观测量。 |
| [Q03] | DST 与状态更新 | `dialogue state tracking update carry over correction dontcare none dialogue state`；`DSTC2 changed goal requested slot label baseline` | 固定版本实现、DSTC2 或同类任务的规范和标注、作者模型论文；定位更新方程、状态标签及评价脚本。 |
| [Q04] | POMDP 与决策 | `POMDP spoken dialogue management Williams Young belief state summary space clarification`；`POMDP dialogue policy belief update computational approximation` | 原始论文或作者公开稿的状态空间、观测模型、后验更新、奖励、策略与近似，必要时补公开实现或作者勘误。 |
| [Q05] | 规则、画像与生命周期 | `spoken dialogue systems user model preferences rule database cross session travel restaurant personalization`；`task oriented dialogue persistent user profile temporary constraint conflict preference` | 原始系统论文、作者数据模型、官方设计或实验；记录存储对象、键与作用域、写入触发、例外、纠正和跨会话条件。若资料仅报告个性化效果，机制缺项单独登记。 |
| [Q06] | 方案对照与混合系统 | `neural dialogue state tracking recurrent hidden state Henderson Thomson Young explicit belief`；`neural dialogue state tracker recurrent LSTM slot distribution hybrid inspectable state` | 原始模型论文、作者代码中的递推和显式输出、公开的一手复现。区分隐状态携带信息和神经网络输出显式状态，追踪两者如何接入下游。 |
| [Q07] | 封闭任务实证 | `DSTC2 handbook results baseline joint goal accuracy statistical significance dialogue state tracking`；`POMDP dialogue manager rule baseline task success latency user study` | 官方评测协议、原始结果表和实现。记录数据、划分、ASR/NLU 输入、模型与预算、基线、指标、结果、显著性、误差和限制，未报告项标明。 |
| [Q08] | 泛化、反例与失效 | `dialogue state tracking unseen slot unseen value new domain schema change schema-guided dialogue open vocabulary`；`MultiWOZ TRADE unseen slot value zero shot error analysis data correction` | 原始基准论文、标注修订和一手复现，必要时查 SGD、MultiWOZ 或相同协议下的研究。分别定位未见值、槽、域、动作和带时间例外的偏好，复核数据泄漏、同域对照及失败案例。 |
| [Q09] | 迁移、状态发现与开放问题 | `language model dialogue state tracking unseen schema zero-shot schema induction slot discovery evaluated downstream`；`conversational memory learning what to remember implicit user preference future task outcome evaluation` | 作者论文、公开实验协议、数据划分、消融与代码。分开登记候选 Schema、监督信号、生成的新状态类别、跨会话的存储选择及未来表现。 |
| [Q10] | 外推边界与长期记忆 | `dialogue state tracking multi-session persistent preference user profile transfer external state context`；`multi session dialogue memory personalization future task controlled study` | 作者系统设计与受控比较，标出持久化、召回、参数、上下文和知识库的角色，比较会话内指标与跨会话下游指标的条件。 |
| [Q11] | 可复查案例 | `DSTC2 dialogue logs annotation labels system acts corrections error analysis`；`MultiWOZ corrected annotations evaluation script dialogue examples joint goal accuracy` | 原始对话数据、作者标注规范、官方评分代码及勘误。固定对应版本，分开原文实例和研究者基于原文的机制推演。 |

## 检索语言、版本与替代路径

- 主检索用英语。用中文关键词“任务型对话 槽填充 对话状态跟踪 隐含偏好”发现术语差异和遗漏；进入证据账本的技术事实回到发布机构、作者或一手复现。保留关键术语原文。
- 优先检索 1990 年代起的早期系统资料，并以更早材料作为必要的历史回溯线索。按问题追踪统计或神经 DST、跨域、开放值、Schema 与 LLM 的后续研究直至截止日。数据和代码锁定发布标签、数据修订号或提交 ID。对采用的来源记录首发、实际版本和取证日期；版本修订或勘误单列。
- 出版页无法访问时转向作者公开稿、会议公开库、机构仓库或同版预印本。若版本不同，核对段落、公式、表号和更改。代码缺失时可用官方评分规范、论文补充材料和可定位的一手复现补充，标明各自可回答的机制问题。关键原文或可替代的一手材料仍缺失时按来源阻塞登记，保留尚需哪类证据及重试路径。

## 反证和遗漏风险

| 待检验的判断 | 应主动寻找的反证或限定 |
| --- | --- |
| 显式槽位在有界任务下更高效且更可控 | 同协议规则、神经和混合基线的成本、状态准确、任务成功和错误恢复证据；只报告精度的论文不能支撑成本判断。 |
| Schema 一开放便必须新增槽或重写状态结构 | 追查开放值、动态 Schema 描述、未见槽迁移以及仍能复用显式结构的实例；说明哪些变化来自原有 Schema 的表达能力。 |
| 隐状态路线与显式状态路线可以互相替代 | 寻找带显式槽分布或跨轮可持久化状态的神经系统，并分开模型表示与接口输出。 |
| 跨域跟踪或 LLM 取值说明模型已会选择记忆 | 查找预先提供 Schema、泄漏、短会话协议、无未来表现消融等限制，也主动寻找真的比较自主保存策略对未来决策影响的研究。 |
| 状态错误意味着系统忘记了已保存的信息 | 检查识别、输入噪声、标注修订、重置、错误更新、状态注入以及策略使用，避免把不同环节归于一种故障。 |

## 检索停止条件

1. 每个必要问题至少记录能定位到原文的候选证据、适用条件和反证路径，完成定向检索后核验能否支持问题。比较性问题优先收集同协议的一手基线和原始实验，协议不一致时分别呈现。
2. 实证归纳可回查任务、数据版本、输入、模型、预算、基线、指标、原始结果和统计报告情况。存在已知版本冲突、数据修订或相反结果时，记录差异及是否影响归纳。
3. 对开放问题可限定到已查原文所能回答的范围，记录未评估的能力及查找过的路径。必要问题仍缺一手证据或关键条件时保留补证动作，不能由可选实例替代。连续检查主要会议或项目源、作者版本和反向检索后没有改变结论的新增材料，可结束已覆盖问题的检索。
4. 完整治理、索引设计和工具轨迹不单独设问题，因为它们不影响 EP01 对状态表达、更新和决策的核心判断。仅在辨别生命周期和外推边界时使用后续议题作为术语参照。
