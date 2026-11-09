# 运行与恢复

命令中的 `WORKFLOW` 指本 Skill 的 `scripts/workflow.py` 绝对路径。`RUN` 使用命令返回的 `run_dir`。在 Codex 中由 Skill 负责取证、写作和审核协调，CLI 负责状态和校验。

```sh
python3 "$WORKFLOW" index --outline "$OUTLINE" --expected-topics 9 --expected-episodes 36 --output-dir "$OUTPUT"
python3 "$WORKFLOW" start --outline "$OUTLINE" --episode EP01 --mode research --as-of-date 2026-11-09 --output-dir "$OUTPUT"
python3 "$WORKFLOW" status --run "$RUN"
python3 "$WORKFLOW" advance --run "$RUN" --stage BRIEF_READY --attempt 1
```

| 模式 | 执行 |
| --- | --- |
| `plan` | `start --mode plan`，完成 `PLAN_READY` 后返回 Brief、范围和计划。 |
| `research` | `start` 或接续现有运行，直到 `ACCEPTED` 或阻塞。通过后导出资料包。 |
| `review` | 读现有运行的 `status`，仅在审核阶段运行独立审核并记录结论。 |
| `resume` | `status` 显示未暂停时继续下一阶段。若已暂停，用 `resume --run "$RUN" --reason "已补证"` 恢复。 |
| `release` | `release --run "$RUN"` 验证清单、实际文件及审核快照并导出。 |
| `batch` | 用 `batch --outline "$OUTLINE" --episode 'EP01..EP04' --output-dir "$OUTPUT" --as-of-date DATE` 规划，支持完整主题标题。用 `start --mode batch` 逐期执行，保持同一大纲、输出根目录和截止日。 |

`deep` 完整复原关键机制，`focused` 收紧例子和可选路线。两个深度档位使用同样的审核门槛。可传 `--writer-id`、`--max-revisions`、`--review-profile standard-v1|strict-v1`。相同参数、大纲及 Skill 指纹得到相同运行 ID。新大纲或 Skill 版本启动独立运行。旧运行的已验收快照仍可验证和导出。

总数校验适用于 `index`、`start` 与 `batch`。换课时传入该课预期值或省略两个总数参数。

一个运行一次由一位写作者负责。阶段收件路径会随尝试变更。若工具或来源故障中途暂停，只从旧收件目录复制已核验、与当前阶段一致的工作文件。`resume` 返回的事件里有 `prior_inbox`。已通过的检查点自动保留。确定性校验失败的阶段和原因写入清单，修正后可在同一收件目录重试。外部材料的到访限制、查询、日期和失败分类写进检索日志。

- 使用 `pause --run "$RUN" --kind tool|source|quality --reason REASON --remedy ACTION` 记录问题。工具可限次重试或换可访问的一手来源。资料缺失须补证。每次质量修订计入配置上限。
- 使用 `rewind --run "$RUN" --to PLAN_READY --reason REASON` 使来源和下游失效。仅修正文稿时，回退到 `EVIDENCE_BUILT`，保留已验证来源和账本。回退保留旧快照和修改事件。补完后按新收件目录提交，审核重新绑定快照。
- 使用原启动参数再加 `--force-refresh-sources --refresh-id REFRESH_KEY` 创建独立的刷新运行。原运行存在有效 Brief 和计划时复用这两步。新的来源核验和所有下游阶段重新执行。
- 使用 `conflicts --run "$RUN"` 比较当前概念登记与同一课程和截止日的已验收稿。批量队列包含显式前置期。单期试点可用大纲中的前置摘要进行研究，并在 Brief 和审核中标明哪些上游尚未有验收稿。发现上游实质错误时登记期数、旧主张编号、证据及受影响的下游。
- 导出的 `manifest.json` 记录文件哈希、运行版本、参数和审查信息。已导出的版本保持独立。对外分享时选资料包及需要的备查文件。将运行目录和草稿留在本地。
