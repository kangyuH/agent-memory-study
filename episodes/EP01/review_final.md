# EP01 最终资料包独立审核

**通过，98/100。** 本报告绑定第 12 次收件的 15 份文件，终审会话为 `ep01-final-refresh-12-86f4e2ab`。与上次终审逐项比较，问题清单、范围、检索计划和概念登记的五份文件哈希一致。主文只改动 Q03、Q04 和 Q09 的四段，证据账本的变更限于 C05、C08–C10、C27 和 C40。本次重开变更涉及的原文，对其余主张沿用此前独立终审的原文核验，并检查现有来源和条件是否保留。

## 逐题核验

| 题目 | 复查结论与原文定位 |
| --- | --- |
| Q01 · 有界任务 | ATIS 的 OAG 数据和旅行场景、PEGASUS 的语义框架与实际 SABRE 接口支撑业务边界。保持词级递推与外部服务契约各自的角色。C01–C03、C15、C21、C37。[S01 Corpus Design](https://aclanthology.org/H90-1021.pdf#page=2) · [S02 System Manager](https://aclanthology.org/H94-1037.pdf#page=2) |
| Q02 · 观测、状态与决策 | DSTC2 的三类输出和 SGD 另设的活跃意图继续分开。离线状态命中与业务反馈分别定位。C02–C04、C06、C08、C11、C16、C23、C34、C38。[S03 §2](https://aclanthology.org/W14-4337.pdf#page=2) · [S09 v2 Model Architecture](https://arxiv.org/pdf/1909.05855v2#page=6) |
| Q03 · 显式更新 | 手册定义目标与搜索方式的旧项系数 `q(c,t) = 1 − Σ_v SLU(t,c,v)`，首轮以本轮 SLU 初始化，后续以新证据加权旧项，无证据时保留旧项，证据质量为 1 时由新证据替换。系统告知请求字段时可重置相应分数。成果论文刊载的系数为证据和，资料分列两种写法。SGD 的三种状态及 Diable 的删除、覆盖和无操作保持各自定义。C04–C07、C15、C18、C19、C35、C38。[S19 §5.1–5.2](https://raw.githubusercontent.com/matthen/dstc/master/handbook.pdf#page=11) · [S03 §3.2](https://aclanthology.org/W14-4337.pdf#page=5) · [S17 v3 §3](https://aclanthology.org/2023.findings-acl.615v3.pdf#page=4) |
| Q04 · POMDP | §2.1 信念更新和语音信箱的 ask、doSave、doDelete，§2.2 的因子化，以及 §4.5 的 Summary POMDP 定位正确。语音信箱低置信区用 ask，confirm 属 §4.1 旅行仿真。检索日志记录引言所指 §4.4 与正文标题有别。C08–C10。[S04 Table 4、Fig. 3](https://www.microsoft.com/en-us/research/wp-content/uploads/2016/02/williams2007csl.pdf#page=6) · [S04 §4.1](https://www.microsoft.com/en-us/research/wp-content/uploads/2016/02/williams2007csl.pdf#page=18) · [S04 §4.5](https://www.microsoft.com/en-us/research/wp-content/uploads/2016/02/williams2007csl.pdf#page=27) |
| Q05 · 画像与规则 | MATCH 的用户无关属性树、注册时取得的个别权重及候选排序可追溯。PEGASUS 的任务局部记录、后端撤销与默认覆盖的研究归纳分开。C02、C11、C12、C30、C32、C38。[S05 §§3.1–4](https://www.inf.ed.ac.uk/teaching/courses/nlg/readings/MATCHCogSci2004.pdf#page=9) · [S02 Dialogue Management](https://aclanthology.org/H94-1037.pdf#page=3) |
| Q06 · 隐状态和显式状态 | 保留 1995 技术报告与 1997 期刊 LSTM 版本的区别，遗忘门证据另列。词级 RNN 同时递推显式槽分布与内部向量，focus 的规则来源更新为手册与成果论文对读。C05、C07、C13–C15、C17、C19、C34。[S18 署名页](https://people.idsia.ch/~juergen/FKI-207-95ocr.pdf#page=3) · [S08 §3.3](https://aclanthology.org/W14-4340.pdf#page=3) |
| Q07 · 准确率、成本与真实结果 | 三个 DSTC2 结果仍分列输入和集成条件，三组结果未并用其他集成比较的显著性。Diable 的完整输入计时、PEGASUS 10 次真实订票中 7 次成功与成功样本耗时分别登记。C05、C07、C09、C16–C18、C20、C22、C23、C25、C31、C33、C36–C39。[S03 Appendix A](https://aclanthology.org/W14-4337.pdf#page=9) · [S08 Table 2](https://aclanthology.org/W14-4340.pdf#page=7) · [S17 v3 Table 2](https://aclanthology.org/2023.findings-acl.615v3.pdf#page=6) · [S02 Evaluation](https://aclanthology.org/H94-1037.pdf#page=4) |
| Q08 · 新值、新槽和新域 | TRADE 与 SGD 的较低留出域或服务结果仍和正例并列。SGD PDF 固定 v2。GenDSI 的 34 个旅行相关重叠域过滤写明，归纳字段和可执行操作仍分别取证。C01、C06、C07、C12、C19–C22、C24、C26–C29、C39、C40。[S10 Table 4](https://aclanthology.org/P19-1078.pdf#page=7) · [S09 v2 Fig. 7、Table 5](https://arxiv.org/pdf/1909.05855v2#page=7) · [S13 §4](https://aclanthology.org/2024.sigdial-1.27.pdf#page=4) |
| Q09 · 给定结构、归纳结构与信息选择 | 给定 Schema 的 IC-DST、GenDSI 的状态推断和聚类、DOTS 同条件比较、Memory-R1 的写入选择各有可复核指标。重读 S13 §4，主 GenDSI 行排除与 MultiWOZ、SGD 旅行相关域重叠的 34 个 D0T 域。重读 S14 §6，十个场景分别评估，指标跨场景和三次重复平均。三组分数、0.5 匹配阈值、冗余槽计数和文本问答边界均保留。C21、C24–C33、C39、C40。[S12 Table 1](https://aclanthology.org/2022.findings-emnlp.193.pdf#page=6) · [S13 §4](https://aclanthology.org/2024.sigdial-1.27.pdf#page=4) · [S14 §6](https://aclanthology.org/2026.tacl-1.5.pdf#page=8) · [S14 Table 6](https://aclanthology.org/2026.tacl-1.5.pdf#page=10) |
| Q10 · 跨会话边界 | MSC 第 2 会话开场困惑度和预测摘要 5% 子采样不变。Memory-R1 改造问答、oracle 设置、对抗子集排除与训练窗口 24/50 回合的原文差异仍分开记录。C03、C11、C12、C14、C16、C30–C34。[S15 Tables 4–5](https://aclanthology.org/2022.acl-long.356.pdf#page=5) · [S16 Table 1、Appendix B](https://aclanthology.org/2026.acl-long.583.pdf#page=14) |
| Q11 · 可追溯失败 | 保留 DSTC2 目标变化、MultiWOZ 2.4 标注修订与模型预测错误、PEGASUS 重复去程的原始材料。缺口限定为同一真实任务中独立替换识别、跟踪和策略且可观察业务后果的受控复测。C22、C23、C35、C37、C38。[S03 Appendix B](https://aclanthology.org/W14-4337.pdf#page=10) · [S11 Table 8](https://aclanthology.org/2022.sigdial-1.34.pdf#page=10) · [S02 Evaluation](https://aclanthology.org/H94-1037.pdf#page=4) |

## 上次终审问题闭合

| 上次终审 | 本次材料审核记录 | 核对结果 |
| --- | --- | --- |
| I13 · focus 作者手册 | I03、I15 | S19 已入来源索引、检索记录、C05、证据矩阵、技术笔记及正文，保留论文刊载差异和脚本未核验范围。重新计算采用 PDF 的 Git blob，匹配 `0045280c679d6eb4d7efe5d45cf71ef2b09bf551`。ACL 2013 年 10 月 8 日公告列明手册可用。[S19 固定版本](https://github.com/matthen/dstc/blob/7897c9beb5fe21fdfb57dcbe1e8f8294c2bcdead/handbook.pdf) · [ACL 公告](https://www.aclweb.org/portal/node/1680) |
| I14 · 语音信箱动作及定位 | I13、I14 | Q04、C08–C10、技术笔记、证据矩阵和 S04 索引均已复核。Table 4 的询问代价归 ask，旅行仿真另有 confirm，因子化与 Summary POMDP 采用正文 §2.2、§4.5。[S04 语音信箱](https://www.microsoft.com/en-us/research/wp-content/uploads/2016/02/williams2007csl.pdf#page=6) · [S04 旅行仿真](https://www.microsoft.com/en-us/research/wp-content/uploads/2016/02/williams2007csl.pdf#page=18) · [S04 Summary POMDP](https://www.microsoft.com/en-us/research/wp-content/uploads/2016/02/williams2007csl.pdf#page=27) |
| I15 · SGD 版本链接 | I16 | `references.md` 和 `sources.json` 均改为可读取的 v2 PDF，版本历史继续可核对。[S09 v2](https://arxiv.org/pdf/1909.05855v2) · [arXiv 版本历史](https://arxiv.org/abs/1909.05855) |
| I16 · GenDSI 和 DOTS 条件 | I17 | Q09、C27、C40 和证据矩阵均记录了训练域筛选和取平均的条件。表值不变，两个协议仍分别解读。[S13 §4](https://aclanthology.org/2024.sigdial-1.27.pdf#page=4) · [S14 §6](https://aclanthology.org/2026.tacl-1.5.pdf#page=8) |

当前材料审核的 I01–I09、I11–I17 均有闭合记录。I10 的 Q11 可选缺口继续接受。S19 封面署 2013 年 9 月，固定 PDF 的生成元数据标示 2014 年 11 月。同期公告可给出手册公开时间的上界。固定提交和 blob 标识本次采用文本，其字节是否与 2013 年发布件相同仍无证据。现有版本记录已注明封面日期、固定提交和公开公告，足以追溯 C05 的公式。记为 I18，接受该版本史缺口。

## 快照和包内链接

复算 15 份文件的 SHA-256，并与工作流返回的值逐项比对。12 个相对链接的目标均存在于候选包。`references.md` 的 S01–S19 在同一张表，条目与 `sources.json` 对应，`coverage.json` 登记 10 个必答题和 1 个可选题，40 项主张和 19 项来源编号均可解析。当前课程输出无已发现的跨期冲突，EP01 无显式前置。

外链复核使用 S19 已取得的固定 PDF 与可检索的公开副本，GitHub 固定文件和仓库网页在本次网页检索环境中未能直开。部分 DOI 重定向和 Wiley 备用页也有访问限制，相关一手正文仍可定位。待验收阶段生成验收报告和发布清单。事实 30/30、覆盖 29/30、机制 15/15、条件 15/15、可追溯 9/10，全部硬门槛通过。
