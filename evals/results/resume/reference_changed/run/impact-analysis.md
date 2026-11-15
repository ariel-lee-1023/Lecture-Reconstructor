# 恢复版本差异与影响分析

记录UTC：2026-11-15T02:21:33.446305+00:00。本次新上下文没有上次生成过程，仅读取当前包和本分支落盘文件。

实际检查：首次误将run目录作为run.json参数，退出1（RUN_READ）；改为`python3 package/scripts/check_run.py run/run.json --repo-root package`后退出2，RUNTIME_CHANGED。输入、SKILL及其他记录runtime文件哈希未变；reconstruction-workflow.md旧哈希为d4330c05bc80cb47834ba627f2a4290d004a2b2ad48bd85bc352586a91af66e3，现为07a2fa38245585dc499dbd47b1ad7c34015a199a3790421fff32a3d9e1b08f07。

当前文件末尾增加“本轮恢复复核：时间条件案例须逐项核对事件名称、时刻与规则触发点，不能仅核对数字是否相同。”将这一精确后缀去掉再计算哈希得到d4330c05bc80cb47834ba627f2a4290d004a2b2ad48bd85bc352586a91af66e3，与旧记录一致。这提供了差异定位的哈希证据；没有读取旧包或其他分支。

影响不是规则内容改变，而是复核方法提高要求。第一章涉及周一确认、周三10—12点，必须重审事件与时刻关联；第二章L2以到达而非发出触发撤销，以及L3封闭/恢复/届满，须逐项核对；第三章有效时段重叠、得知次日起算与申请到达、17:59变式依赖这些事实，必须纳入新复核。故对全课结构和三章都重新检查。已存在第一章由reviewed降为needs_review；计划中两章亦标needs_review并如实记尚无正文，待生成后复核。

旧语义chapter-1 pass保存于history/before-resume及before-resume-run.json，原章SHA不改。当前记录使旧语义记录失效为not_run，保留原status、date、evidence及旧章hash在historical_checks中；旧full_manuscript本来就是not_run，绝不借用。旧机械通过仅属旧断点，当前也不沿用。invalidated-run.json在更新runtime哈希前落盘，因此可核验失效先于刷新。

逐项检查的重点：戊17:50发出/18:05到达；己18:00到达；庚周二17:58发出/18:02收到；周三10—11封闭/11恢复/12届满；壬9:30—10:30封闭与10—12预约；癸周四得知/下周四到达；庚周四得知/下周三申请且到达；变式17:59到达。完成这些检查及全篇直接对源复核后，才可恢复完成状态。

快照保存在本run内history独立目录，符合本分支仅可写run的范围限制；未写包、上游、其他分支。
