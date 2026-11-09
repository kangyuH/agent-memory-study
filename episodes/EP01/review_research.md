# EP01 材料增量审核

**通过。** 本次会话为 `ep01-pr5-materials-amend-6f23e161`，复核发布版本 `008d813ef5941de9` 的局部勘误。原始审核分数和未变更部分的核验记录沿用前版。本次绑定的是修订后的文件快照。

## PR #5 材料增量复核

会话 `ep01-pr5-materials-amend-6f23e161` 通过本次复核，重新计算工作流规定的 13 份材料哈希。与上一版已验收资料比较，差异限于账本、矩阵、研究主文和两个来源索引文件中的 C04、C06、C25、C31。沿用前次逐题审核对未改动主张的结论。本次另抽查 Q08–Q11 的 TRADE、GenDSI、DOTS、MSC、Memory-R1 和原始失败样例，10 个必答题仍已覆盖，Q11 保留同一真实任务受控复测的缺口。

- I19 已关闭。DSTC2 的 §2.1 支持修订后的请求字段定义，§2.3 Table 2 和附录 B 支持目标约束可变。 [DSTC2 原文](https://aclanthology.org/W14-4337.pdf#page=2)
- I20 已关闭。SGD v2 的 User Goal 段及式 (6)–(9) 区分保留旧值、写入无偏好和进一步预测值。 [SGD v2 原文](https://arxiv.org/pdf/1909.05855v2#page=6)
- I21 已关闭。IC-DST 的 §4 和 Table 1 继续支持两版 MultiWOZ 结果，1% 示例池与每提示 10 或 5 个示例分别核对。 [IC-DST 正式版](https://aclanthology.org/anthology-files/pdf/findings/2022.findings-emnlp.193.pdf#page=6)
- I22 已关闭。MSC 的 §5 和 Tables 4–5 支持预测摘要 5% 子采样条件及第 2 会话开场结果。 [MSC 正式版](https://aclanthology.org/2022.acl-long.356.pdf#page=6)

---

以下是前版审核原文，所列收件批次、快照和检查均对应前版。

# EP01 研究资料独立复审

**通过，98/100。** 本次复查来源刷新运行第 11 次收件，独立审核会话为 `ep01-materials-refresh-11-b7e6d9a2`。以本运行第 6 次收件审核为对照，重算两份快照的全部 13 个绑定文件哈希。7 个文件有差异，均属本轮修订。Q01–Q11 与 C01–C40 的审核范围完整。I01–I09、I11–I12 的闭合延续，I10 的可选缺口继续接受。I13–I17 均已修复。

## 初审问题复查

| 问题 | 状态 | 复查结果与定位 |
| --- | --- | --- |
| I01 · DSTC2 归源 | 已修复 | S08 Table 2 的 h-ASR 和 h-SLU 分别为 0.768/0.346、0.742/0.387；§5 核实各集成 12 个跟踪器并说明输入差异。S03 §3.2 确认 focus 为 team0.entry1，Appendix A 对应 0.719/0.464。Q07 表和 C17 分开归源，S03 Table 4 的检验仍明确只属于另列集成比较。[S08 §5、Table 2](https://aclanthology.org/W14-4340.pdf#page=6) · [S03 §3.2、Appendix A](https://aclanthology.org/W14-4337.pdf#page=5) |
| I02 · SGD 槽状态 | 已修复 | S09 Eq. (6) 上下文列出 `none`、`dontcare`、`active`；Q03、C06 和技术笔记已按该契约书写。技术笔记区分活跃意图的 NONE 和另一个系统 Diable 的整轮无操作。[S09 v2 Slot Status Prediction](https://arxiv.org/pdf/1909.05855v2#page=6) · [S17 v3 §3](https://aclanthology.org/2023.findings-acl.615v3.pdf#page=4) |
| I03 · focus 更新式 | 已修复 | S19 §5.1 直接给出余量系数及两个边界，S03 §3.2 则刊载证据和。C05、Q03 及技术笔记分列两份原文，未把手册规则写成已核实的脚本实现。[S19 §5.1–5.2](https://raw.githubusercontent.com/matthen/dstc/master/handbook.pdf#page=10) · [S03 §3.2](https://aclanthology.org/W14-4337.pdf#page=5) |
| I04 · GenDSI 实验 | 已修复 | Q09 和 C27 分开 Table 1 的人工状态推断与 Table 2 的聚类诱导。前者每测试集各抽 60 条留出域话轮，D0T 三行的完整性/正确性为 T5-SGD 32.3/72.6、GPT-D0T 93.3/82.0、T5-D0T 95.7/81.2。训练分布和 Agresti–Caffo p < 0.05 的同列标记已保留。后者 MultiWOZ 2.1 验证集的槽/值 F1 为 90.9/70.5、180 诱导槽对 31 个参考槽，USI 在两个指标上的排序方向不同。[S13 Tables 1–2](https://aclanthology.org/2024.sigdial-1.27.pdf#page=3) |
| I05 · 首次公开与采用版本 | 已修复 | S18 为 Hochreiter 与 Schmidhuber 的 TUM FKI-207-95 技术报告，署 1995-08-21；S06 和 C13 的单元机制仍定位 1997 年期刊版。S14 预印本为 2025-04-25，数值沿用 TACL 2026；S17 固定 ACL v3，保留 2023-05-26 预印本记录。S03 的 2014 年成果论文与 2013 年公开挑战已分列。[S18 原件](https://people.idsia.ch/~juergen/FKI-207-95ocr.pdf#page=3) · [S06 期刊版](https://doi.org/10.1162/neco.1997.9.8.1735) · [S14 预印本](https://arxiv.org/abs/2504.18474) · [S17 版本索引](https://aclanthology.org/2023.findings-acl.615/) · [DSTC2 发布通知](https://www.aclweb.org/portal/content/second-dialog-state-tracking-challenge) |
| I06 · 真实任务与交易失效 | 已修复 | C37 入账 S02 的 8 名组员、10 次真实往返订票、7 次完成和 6 名成功参与者。Table 1 的 24.5 次查询及 814 秒为成功订票的均值，便利样本无随机对照。C38 与 Q11 分开报告应用清除历史、未取消后端预订及去程重复预订的实际后果。Q07 将该现场结果与 DSTC2 离线指标和 Diable 模型时延分列。[S02 Evaluation、Table 1](https://aclanthology.org/H94-1037.pdf#page=4) · [S17 v3 Table 2](https://aclanthology.org/2023.findings-acl.615v3.pdf#page=6) |
| I07 · 规则与画像 | 已修复 | S05 §3.1 Fig. 6 为选餐厅的用户无关目标属性树，权重由注册问卷个别赋值；§4 的 SPUR 对符合查询条件的候选排名并选择展示内容。C11 已收窄任务模型表述。S02 区分票据框架、临时候选、重置与 `scratch that` 的撤销请求；Q05 把通用优先级和过期规则列作归纳。[S05 §§3.1–4](https://www.inf.ed.ac.uk/teaching/courses/nlg/readings/MATCHCogSci2004.pdf) · [S02 Dialogue Management](https://aclanthology.org/H94-1037.pdf#page=3) |
| I08 · 迁移与归纳反证 | 已修复 | S10 Table 4 的 taxi 60.58%、hotel 13.70%、train 22.37% 及单域全量参照已分别记录。C39 与 S09 Fig. 7/Table 5 一致，未见 RentalCars、Buses 的 Joint GA 为 0.086、0.097，见过的 Weather 为 0.620，RideSharing 也只有 0.170。C40 在 DOTS、Ll-8B、FINAL 的行内对比为 Embed 46.2/74.8、Revision 57.8/68.2、Slot Conf 66.8/74.9。正文保留先诱导最终 Schema 再回放、模拟且人工校对测试材料，并且分别解读槽和值。未把 S13 旧指标与 S14 新指标做数值横比。[S10 Table 4](https://aclanthology.org/P19-1078.pdf#page=7) · [S09 Fig. 7、Table 5](https://arxiv.org/pdf/1909.05855v2#page=7) · [S14 §§5–7、Table 6](https://aclanthology.org/2026.tacl-1.5.pdf#page=10) |
| I09 · 多会话条件 | 已修复 | S15 Table 5 确认 Table 4 的预测摘要行使用 5% `no-summary` 子采样。S16 Appendix B.1 说明其 MSC 为改造问答，LongMemEval 用 oracle。B.2 段落和 Algorithm 1 各写 24 和 50 轮，C32 与 Q10 原样标明冲突；LoCoMo 同 Qwen 底座的 SFT、GRPO、PPO 结果和排除对抗题仍可定位。[S15 Tables 4–5](https://aclanthology.org/2022.acl-long.356.pdf#page=5) · [S16 Table 1、Appendix B](https://aclanthology.org/2026.acl-long.583.pdf#page=14) |
| I10 · 受控反事实 | 继续接受 | Q11 仍为可选部分覆盖，已含 DSTC2 标注和示例跟踪输出、MUL1697 订位标签与预测、PEGASUS 真实后端后果。三种材料没有在同一真实任务上控制识别器、跟踪器和策略，因果归因及故障发生率仍超出所查材料。[S03 Appendix B](https://aclanthology.org/W14-4337.pdf#page=10) · [S11 Table 8](https://aclanthology.org/2022.sigdial-1.34.pdf#page=10) · [S02 Evaluation](https://aclanthology.org/H94-1037.pdf#page=4) |

## 按冻结清单复查

| 题目 | 本次复查 |
| --- | --- |
| Q01 | ATIS 的固定业务范围、PEGASUS 的真实后端、概率与神经路线的作用环节保持可追溯。早期论文、挑战和后来采用版本分别记录。 |
| Q02 | 语义提取、任务状态、策略和持久化仍为可观察的不同接口。补充的 PEGASUS 证据支持区分状态重置和执行结果。 |
| Q03 | 保留、无偏好、覆盖、删除和竞争候选分别按实现解释。作者手册的 focus 公式、初始化及重置已经直接取证，与 S03 的刊载差异分列。 |
| Q04 | S04 的信念更新、因子化与 Summary POMDP 分别定位 §2.1、§2.2 与 §4.5，语音信箱的询问与旅行仿真的确认分开，见 I13–I14。 |
| Q05 | 用户目标树、注册画像、局部状态和业务动作各有直接来源；持久规则适用范围与一次性覆盖属于有边界的归纳。 |
| Q06 | 1995 技术报告用于版本，1997 期刊版用于机制；遗忘门和词级 RNN 的双状态接口保留各自条件。 |
| Q07 | 公共日志离线匹配、实现吞吐、模型计时、真实订票成功和现场失败分别记录。三组 DSTC2 结果无统一成本或成对显著性。 |
| Q08 | 区分新值、未见服务、诱导新字段和新动作；有低分反例和条件，不将迁移结果外推到真实动作。 |
| Q09 | 给定 Schema 取值、归纳候选类别、学习跨会话写入分别有实证；旧基准知识对照和后续任务收益的边界均保留。 |
| Q10 | 预测摘要和跨会话问答有各自模型、任务和指标；公开的训练窗口冲突未被误写成唯一实现。 |
| Q11 | 多个原始回合和真实失败补足诊断材料，受控反事实缺口仍限定在同一真实任务。 |

## 第 16 次收件差异复查

- **I11 已修复。** C40 的证据定位和实验条件、证据矩阵及 Q09 已补 S14 §5.2 和 Table 5 的测量口径。每个预测槽与最相似的金标槽比较，依据忽略大小写的精确值匹配比例，相似度达到 0.5 才保留映射。槽精确率分子按不同金标槽计数，分母仍为所有预测槽，冗余预测因此计入误差。Table 6 的三组同条件结果没有变化，Q09 明确区分 S13 的匹配与计数规则。[S14 §5.2](https://aclanthology.org/2026.tacl-1.5.pdf#page=7) · [S14 Table 5](https://aclanthology.org/2026.tacl-1.5.pdf#page=8) · [S14 Table 6](https://aclanthology.org/2026.tacl-1.5.pdf#page=10)
- **I12 已修复。** `references.md` 的 S17 和 S18 之间的空行已去除。按 GFM 解析，S01–S18 均在同一张表内，S18 原文链接及 C13、`sources.json` 的引用保持完整。[S18 原件](https://people.idsia.ch/~juergen/FKI-207-95ocr.pdf)

## 来源刷新差异

- **S19 与 C05。** 独立重算 PDF 的 Git blob，和索引记录的 `0045280c679d6eb4d7efe5d45cf71ef2b09bf551` 一致。重新读取手册印刷页 10–12，确认 §5.1 定义目标、方式组件的 `q(c,t) = 1 − Σ_v SLU(t,c,v)`，首轮用本轮 SLU，后续以新证据加 `q(c,t)` 乘旧状态。原文示例给方式旧项权重 0、区域旧项权重 0.7，且区分请求字段在系统告知相应槽时可重置分数。§5.2 给出脚本入口，未核对脚本实现。S03 §3.2 刊载式与此有差异。GFM 解析确认 S01–S19 同表，C40 更新只同步大小写无关的匹配口径。[S19 固定 PDF](https://github.com/matthen/dstc/blob/7897c9beb5fe21fdfb57dcbe1e8f8294c2bcdead/handbook.pdf) · [S19 §5.1](https://raw.githubusercontent.com/matthen/dstc/master/handbook.pdf#page=10) · [S03 §3.2](https://aclanthology.org/W14-4337.pdf#page=5)
- **I13 已修复。** S04 来源索引、C10、证据矩阵及技术笔记采用正文 §4.5，Fig. 23 附近可核对精确信念监控和压缩规划。§4.4 另为使用真实对话资料估计用户模型的仿真。§2.2 的因子化定位正确。[S04 §4.4](https://www.microsoft.com/en-us/research/wp-content/uploads/2016/02/williams2007csl.pdf#page=25) · [S04 §4.5 与 Fig. 23](https://www.microsoft.com/en-us/research/wp-content/uploads/2016/02/williams2007csl.pdf#page=27)
- **I14 已修复。** Q04 以 ask 作为语音信箱的询问动作。S04 Table 4 的询问收益 −1 对应 ask，doSave 和 doDelete 有各自的收益。§4.1 的旅行仿真另含 confirm-to-x、confirm-from-x，提前确认的 −3 仅在用户还未提到该字段时适用。正文、C09 和技术笔记的动作边界一致。[S04 §2.1、Table 4](https://www.microsoft.com/en-us/research/wp-content/uploads/2016/02/williams2007csl.pdf#page=6) · [S04 §4.1 旅行仿真](https://www.microsoft.com/en-us/research/wp-content/uploads/2016/02/williams2007csl.pdf#page=18)
- **I15 已修复。** 固定 PDF 封面为 2013 年 9 月。结构化来源把已证公开年记为 2013，来源索引注明 10 月 8 日的 ACL 公告已列该手册可用，检索日志注明精确首发日期未证。Git blob 已复核，C05 仍由手册 §5.1 直接支撑。[S19 固定 PDF](https://github.com/matthen/dstc/blob/7897c9beb5fe21fdfb57dcbe1e8f8294c2bcdead/handbook.pdf) · [2013-10-08 ACL 公告](https://www.aclweb.org/portal/node/1680)
- **I16 已修复，对应原运行终审 I15。** S09 索引和结构化来源固定为带版本号的 arXiv PDF。重开后核实首页列 v2 和 2020-01-29，继续使用该版的状态术语与未见服务对照。[S09 v2](https://arxiv.org/pdf/1909.05855v2)
- **I17 已修复，对应原运行终审 I16。** S13 §4 Models 的主 GenDSI 行在训练前排除 34 个与 MultiWOZ 和 SGD 旅行相关域重叠的 D0T 域，Table 2 另有全域行。S14 §6 对 10 个测试场景各自测量，再对场景和三次重复取平均。C27、C40、证据矩阵及 Q09 都补齐了对应条件，原表数值未改。[S13 §4、Table 2](https://aclanthology.org/2024.sigdial-1.27.pdf#page=4) · [S14 §6](https://aclanthology.org/2026.tacl-1.5.pdf#page=8) · [S14 Table 6](https://aclanthology.org/2026.tacl-1.5.pdf#page=10)

原运行终审 I13 的手册实证已由本运行 I03 及 S19 复查承接，原运行终审 I14 的章节和动作集合由本运行 I13–I14 承接。I10 仍限于公开材料未提供同一真实任务的受控反事实重放。

主文仍符合 03 的资料组织与下游职责边界。按 standard-v2 计，事实 29/30、覆盖 29/30、机制 15/15、条件 15/15、可追溯 10/10，全部硬门槛通过。
