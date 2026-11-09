# EP01 检索与取证记录

取证日期和截止日均为 2026-11-09。以会议和作者原文为事实入口，按问题分别检查方法、实证和限制。此记录覆盖本次实际查询与定向复核。

| 问题 | 查询或定向检查 | 命中和定位 | 核验结论与边界 |
| --- | --- | --- | --- |
| Q01 | `ATIS pilot corpus Hemphill Godfrey Doddington`、`PEGASUS System Manager` | S01 任务与采集，S02 系统管理器，S03 共享任务 | 固定关系数据库、后端操作与显式状态分工可定位。入选系统用于刻画机制，早期路线只做代表性取样。 |
| Q02–Q03 | `DSTC2 Appendix B requested slots reset previous belief`、`Diable operations on tables` | S03 §§2–4、附录 B，S08 §§3.1–3.4，S09 方法，S17 §3 | 跟踪、状态更新和决策可分别观察。无偏好与未知标签要按基准各自解释。对早期完整日志只引用论文明确展示的信号。 |
| Q04 | `Partially observable Markov decision processes for spoken dialog systems belief Eq. (2) scalability` | S04 §§2–5、Figs. 2–4 | 概率更新与策略可复原。示意回合、仿真和真实用户效果的证据层级分别记录。 |
| Q05 | `Generation and evaluation of user tailored responses multimodal dialogue MATCH database attribute weights` | S05 §§3.2–3.4、Fig. 6，S02 System Manager | 出版网页直开受限，Edinburgh 原文文字层存在编码问题，转用同一 PDF 的截图核对 §§3.2–3.4。任务模型、持久用户模型与临时缓存分列。 |
| Q06–Q07 | `constant error carousel`、`forget gate continual prediction`、`Word-Based 0.768`、`Diable 2.4x more time` | S06–S08、S03 Table 4、S17 §§5–6 | 递推状态和外部接口可同时使用。DSTC2 结果属于离线跟踪，耗时结果使用单独的 MultiWOZ 协议。 |
| Q08 | `TRADE unseen values unseen domain Table 2`、`schema guided non-categorical`、`MultiWOZ 2.4 annotation corrections` | S09–S11 | 未见值、服务迁移和标签修订具有不同验证协议。SGD 出版 PDF 曾触发访问限制，本次实际采用可读 arXiv v2 全文并查对版本历史。 |
| Q09 | `IC-DST schema few-shot Codex`、`slot schema induction generative dialogue state`、`streaming refinement simulated interactions`、`Memory-R1 reinforcement memory operations` | S12–S14、S16 | 显式提供 Schema、自动归纳候选槽、跨会话写入策略属于不同证据。特意检查数据集名提示可诱发 Schema 复述与训练奖励来源。 |
| Q10 | `Beyond Goldfish Memory Multi-Session Chat Table 4`、`Memory-R1 Table 1 training data` | S15 §4 与表 4，S16 §§3–4 和附录 B | 多会话回答可单独测量。记录样本、模型、预算口径与未观察的工具执行结果。 |
| Q11 | 定向检查 `DSTC2 Appendix B`、`MultiWOZ 2.4 Table 8` | S03 附录 B、S11 表 8 | 两处已见原始论文样例。样例提供的信号不足以对同一真实任务独立复测观测器、跟踪器和策略。把这一缺口留在覆盖表。 |

初稿纳入 17 份已打开的一手论文，审核后另纳入 1 份早期技术报告和 1 份作者手册，共 19 份。DOI 和版本记录用于核对同一作品，正文中的结果以列出的采用版本为准。没有运行作者代码或重跑完整基准。来源未披露的统计或开销信息按相应表和章节记录。

## 审核复查

- S03 §3.2 指定 focus 为 team0.entry1，Appendix A 给出精确数值。S08 Table 2 只用于各 RNN 提交。
- S09 的 Slot Status Prediction 按原文记录 none、dontcare、active。
- S13 Table 1 对照 T5-SGD 与 T5-D0T 的训练分布，保留列标和显著性口径。
- LSTM 首发以 FKI-207-95 技术报告署名页为证，MultiWOZ 2.4 首发查对 arXiv 版本历史。
- S02 复查 Evaluation、Table 1 和 Dialogue Management，补齐实际订票结果和清空对话记录后的重复预订案例。
- S05 截图核对 Fig. 6 附近的任务模型是用户无关的目标属性树。
- S14 对照 arXiv:2504.18474 v1 和 TACL 2026；S17 固定 ACL v3 文件并对照 arXiv 版本历史。
- DSTC2 作者发布仓库列出 dstc2_scripts.tar.gz。公开取证入口未取得可读的实现内容，后续找到可读取的作者手册 S19，见下文。
- 追加核对 S09 Table 5/Fig. 7、S10 Table 4 与 S14 Table 6 的留出与同底座行，避免只摘高分；补 S15 摘要采样条件和 S16 Appendix B.2 的窗口冲突。

## 终审新增原文与定向复查

- 已读取 S19 的作者发布手册，固定 Git 提交并核对 PDF blob。第 10–11 页给出 focus 的旧状态权重、初始化及重置。S03 刊载式少了余量项所需的 1−；按两份一手原文分别保留口径。发布压缩包仍无可读实现，本次核对手册定义与原文例子。
- 重新定位 S04 的语音信箱、因子化和旅行仿真。分别登记 §2.1 的 ask 与 §4.1 旅行仿真 的 confirm。
- S04 用正式正文标题确定 Summary POMDP 为 §4.5（Fig. 23 附近）；§4.4 是使用真实数据估计用户模型的演示。引言所标的章节编号与正文标题不同。
- S19 封面署 2013 年 9 月。ACL 于 2013 年 10 月 8 日的公告已将手册列为可用，精确首发日期仍无足够证据。[ACL 发布公告](https://www.aclweb.org/portal/node/1680)
- S09 固定为 arXiv v2 的 PDF。S13 §4 核对 Table 2 训练前排除的 34 个重叠领域，S14 §6 核对 10 个测试场景及 3 次重复的聚合条件。
