# 验证记录

构建日期：2026-11-15（Asia/Shanghai）。结构化状态见 [validation.json](validation.json)，运行核心版本见 [runtime-revision.json](runtime-revision.json)。本记录区分工程检查、实际生成行为、课堂试用和学习效果。

语言规则已按用户要求更新为“明确指定优先，否则采用课程语言”。本次只检查格式、包结构及规则一致性，未重跑模型行为验收。下文A01–A12、匿名对照与恢复结果均属于[更新前版本](runtime-revision.pre-language-policy.json)，[旧验证状态](validation.pre-language-policy.json)及原始运行哈希保持不变。

**Current revision — English runtime and documentation (2026-11-15):** The user requested English versions of the core, four method references, requirements documents, and maintenance agreement. The manuscript language policy is unchanged. Translation changes the model instructions, so the current runtime has new hashes and behavior acceptance remains `not_run`. The [preceding runtime](runtime-revision.pre-english-core.json), [preceding validation status](validation.pre-english-core.json), and all historical evaluation artifacts retain their original identities. Textual equivalence and mechanical checks are not model behavior tests.

For this translation, all 40 unit tests, the repository checker, and the skill-format checker passed. Independent comparison with the prior text identified two wording changes that were corrected: quiz questions remain distinct from clarification, and inspecting the test fixtures remains optional. Source locations, links, record identifiers, and executable examples were checked for preservation. No model behavior scenarios were rerun.

| 状态字段 | 结果 | 证据与范围 |
|---|---|---|
| repository_checks | pass | 40项标准库测试、包结构检查、skill格式检查；见[机械证据](../evals/results/mechanical/summary.json) |
| behavior_acceptance | not_run | The current English runtime has not been behavior-tested; the baseline A01–A12 passes retain their original runtime identities. |
| real_classroom_pilot | not_run | 未提供真实课堂材料；所有实际执行均为明示合成样本 |
| learning_outcomes | not_run | 未测量真实学习者理解、迁移或延迟表现 |

## Historical engineering scope at the initial build

已实现唯一运行入口SKILL、四份自足references、运行schema、两个标准库检查器、维护约定、README、MIT许可、来源manifest及有内容的验收材料。本地Git初始化为main，无提交、远程仓库、推送或全局安装。intent.md与spec.md已同步本次用户指定的语言规则；更新前基线已备份，plan.md登记实施状态。

实际重新核对19份上游文件，哈希均与交接清单一致，HEAD与工作树状态已登记。原书没有在本次重新通读；保留的是实际读取的上游参考摘要中的作者和章节定位。新增讲稿流程、记录接口与验收设计不归为原作者已验证的方案。上游、下载目录未被本次改写。

目标起初为空。工程包在目标外带时间戳目录备份；本机恢复位置见`.work/backup-location.txt`，该目录的`changes-final.json`逐文件记录初始absent与交付哈希。本机来源清单、原始临时执行、备份不进入发布文件集。公开`evals/results/`仅收录本项目合成执行证据；路径脱敏见该目录说明。

## 实际行为与证据

- [三类讲稿独立对照](../evals/results/skill/independent-review.md)：概念、案例、争议课实际全文，覆盖A01–A03、A05–A07；重要小案例、反驳、考试/作业信息、条件、版本和来源归属均核对。
- [边界独立评审](../evals/results/edges/independent-review.md)：实际ASR、注入、百字约束、空输入、失效路径、混乱字幕，覆盖A04、A09、A11、A12。需要澄清的输入保持needs_input，不能把场景通过误写成完整稿已交付。
- [完整包隔离评审](../evals/results/isolated/independent-review.md)：A10使用另一个新上下文、完整复制包、读取白名单实际生成；方法不依赖兄弟仓库。
- [中断编排证据](../evals/results/resume/orchestration.json)：A08真实第一章后结束生成turn，然后三个独立新上下文恢复。原样首次检查0，输入变化与仅reference变化首次检查2。[原样](../evals/results/resume/unchanged-review.md)、[输入变化](../evals/results/resume/input_changed-review.md)、[reference变化](../evals/results/resume/reference_changed-review.md)均已独立逐源复核通过。输入变化分支正确保留needs_input及全篇语义fail，因主案存在文本冲突和结算缺口；该场景的通过不代表主案结算完成。

逐项条件、判定和证据见[A01–A12表](../evals/acceptance.md)。生成与评审使用实际宿主模型；能知道的配置已记录，精确后端、采样参数与token量为unknown。

## 匿名比较

[匿名评审](../evals/results/comparison/review.md)完成后才公开[标签映射](../evals/results/comparison/unblinded-key.json)。概念课与案例课五维相当；争议课中skill版本在新增论证身份、解释理由和代价展开上局部较优，其他维度相当。两种方法都未被评审识别出关键缺陷。普通改写中个别轻微叙事补足和措辞移动保留在原始对照中，没有为了得到优势而改对照稿或评分。

两组继承同一父模型配置，无模型覆盖，但精确后端不可见。各以一个agent turn依次生成三稿；普通改写观察区间约258秒，skill约653秒，包含文件和记录工作，不是纯生成耗时。skill执行了更多记录与检查，且首批包复制时schema尚缺、随后补入；这批不计A10，A10另用完整包重新执行。资源不等、每类仅一份样本且无重复采样，不能将局部偏好独立归因于方法，更不能宣称普遍优于直接改写。详见[资源记录](../evals/results/comparison/summary.json)。

## 检查器与版本整合

40项测试实际检验悬空ID、重复ID、合并环、区间越界、已完成章缺锚点、输入/核心/reference变化、缺失/过期全篇评审、较晚失败评审覆盖旧pass、正常planned与needs_review记录、包内断链与排除依赖等。退出码0只说明有限机械约束，不能判断法律、覆盖语义或教学效果。

三类课生成过程中检查器增加了“较晚全篇失败使旧pass失效”和“全包Markdown断链”检查；运行提示与四refs未变。保留原生成记录、实际差异检测、needs_review中间记录，经原文和完整主稿独立复核后更新检查器身份并重新执行。原始pass没有被直接换哈希沿用。首轮教学参考检查亦将示范例子限定为示范，避免误要求每门课重复同一例子；此调整在全部正式行为生成之前完成。

最终独立工程审阅又复现了一个P2：保留历史pass并为改后稿追加新pass时，旧检查器仍将历史哈希与当前稿比较，错误拒绝完成。已修为只用最新全篇语义记录绑定当前稿；历史哈希格式和证据仍检查。回归同时证明最新stale/fail/not_run仍拒绝。另补通用绝对路径根的检查，避免漏掉/srv等依赖，并检验URL、HTML锚点与相对路径不误报。最终40项测试通过。检查器变动的影响记录随当前run保存；未改教学提示、输入或讲稿字节。

## 证据边界

边界场景由了解设计和验收标准的主编排者生成，再交给无生成历史的评审；三类普通/skill对照、A10和恢复使用新上下文。模型评审提供第二视角，不是正确性的证明。

A09可见内容与真实追加要求已独立检查；编排者观察到未调用邮件、安装或发布工具，但没有完整外部副作用日志供独立系统审计。A10是读取白名单隔离，不是操作系统级沙箱。A08是三章恢复协议，未测试超大上下文极限。这些限制不被写成已验证能力。

独立最终工程审阅发现的P2已修复并定向复核关闭，未识别出剩余关键工程缺陷，见[工程审阅](../evals/results/mechanical/final-engineering-review.md)。这是语言更新前构建基线的验收结论；当前语言规则版本的模型行为未重跑，真实课堂试用与学习效果仍未运行。
