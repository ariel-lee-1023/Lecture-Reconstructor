# 全课重构、记录与恢复

本文件是本项目新增的生产流程；来源中的教学原则不自动推出这些文件格式、阶段或质量门槛。流程服务于完整讲稿，可以按素材组织章节，不要求读者看工程字段。

## 1. 输入与边界：ingest → map

为本次任务建 `.work/runs/<run-id>/`。原始输入保存为 `input/original.*`，规范化文本保存为 `input/transcript.txt`；两者分别计算 SHA-256。粘贴文本也保存快照。规范化只处理编码、字幕结构和必要的可读性，不删除重要文字；保留时间码文本以便追溯，不推测缺失时间。每个 `inputs` 项用 `path`、`sha256` 指向原始文件，用 `normalized_path`、`normalized_sha256` 指向实际建立行定位的文本。相同文本可用同一路径。

空输入或路径失效时记录 `needs_input` 与确切缺口，不生成假课堂。缺少教材、背景画像等不阻止工作。未知课程法域/年代填 `unknown`；假设写进 `course.assumptions`，可撤回。重要含义不明时只问改变判断的最小问题；保存其余可处理内容。

全文读取后，`source_review` 对每个输入的规范化文本记录 1 起算、两端包含的 `start_line/end_line` 和 `reviewed/unread`；这些字段只是读稿记录，不是理解的证明。无需逐句建数据库项，但所有输入行都应有覆盖记录，正文之外的标题和字幕也不能留下误判为未读的空隙。

`content_units` 按实际意义切分：定义、命题、推理、案例、例外、反例、实质疑问、教师考试提示。每项保存稳定 ID、简短命题、输入行范围与短摘录、类型。重构前的暂存项可以为 `unresolved`，说明尚未写作并判断是否 blocking，不能假装已完成。

## 2. 教学规划：plan

建立全课整体问题、章节顺序和术语表，再分章写。每章写入 `learning_object`、`relations`、`prerequisites`、`approach`、`role` 与 `content_unit_ids`。例如学习对象是“同意与请求权的区别”，关系是“免于不当干预不等于对方负有给付义务”；以同一借用事实中授权与承诺的变化作对照。具体正文如何解释，参照 [教学设计](teaching-design.md)。

章使用稳定 ID 与显式 HTML 锚点，如 `<a id="ch-consent"></a>`；细节项可指向节锚点。章文件通常为 `chapters/01-consent.md`。`planned` 允许没有章文件与锚点；写入正文后必须验证其实际存在。新章顺序变动不改 ID；术语决定写 `terms`，同一实体不用近义词随机替换。

长课按完整概念或论证单元分章。只在实际有前后课材料时写跨课衔接。目标篇幅不足以容纳实质内容时，保存完整范围并明确采用分册/配套扩展稿，或提出关键取舍；不得用“精简版”掩盖遗漏。

## 3. 写作与来源：draft

按章写可直接朗读的解释性段落，不输出供别人完成的建议。开场交代本课问题，结尾兑现学习对象，章间解释当前步骤怎样服务全课。例子要分析事实、改变的条件和不变因素；思考题有完整解析。

内容项的处理只用以下状态：

| 状态 | 记录与成稿责任 |
|---|---|
| represented | 已解释，`targets` 指向章 ID 和真实锚点 |
| merged | 与另一项合并；保留原定位，`merge_into` 指向目标内容 ID，`targets` 指实际正文；不能形成环 |
| corrected | 保存 `original_meaning`、修改理由和 `correction_basis`，`source_ids` 关联实际读到的依据，并指向修正后正文 |
| excluded | 写出与课程无关或纯重复等具体理由；不能因困难、篇幅或争议排除实质内容 |
| unresolved | 给出 `blocking` 和 `blocking_reason`；会改变核心论证时须阻止 complete |

`locations` 保留原课定位，`targets` 记录重排后的成稿定位。重要新增命题可新建解释项并关联实际输入或补充来源，但不能为其编造原文行号。没有原课定位的纯补充项用空 `locations`、真实 `source_ids` 与明确新增身份。

`sources` 保存 ID、实际路径或 URL、版本、准确定位和 `read_status`。输入原课也可登记为来源。精确法律事实或学说归属必须有已读支持；教学假设标为假设，解释性推理说明从哪些前提得到。正文保留会影响结论的法域、时间、条件与归属；细节审计放 `notes.md`。查阅链接不等于命题获得支持。

## 4. 每章检查与全篇复核：review → assemble → deliver

章完成先写文件，再把 `chapters.status` 改 `drafted`。检查遗漏与推理后改 `reviewed`，待重审则用 `needs_review`；若文件不在则填 `missing_reason`。全篇统稿处理重复定义、矛盾、术语漂移、未兑现铺垫和突兀衔接，合并到 `lecture.md`，保持目标锚点。

语义复核必须重新对照实际输入与实际主稿，特别检查清单之外可能漏掉的小案例、反驳、考试提示、否定和例外。核对每条重要新增事实的来源身份；判断推理是否完整、对照是否说明关键条件。可用独立评审，但不能用只看成稿的“很好”代替对照。记录评审者身份已知范围、方法、逐项证据和缺陷；未知设置填 `unknown`。

先执行 `python3 scripts/check_run.py .work/runs/<run-id>/run.json --repo-root .`。退出码 0 是结构通过，1 是记录或文件错误，2 是输入/runtime 改变需重审。脚本不会替你判断法律或教学正确性，也不会自动改状态。

`checks` 区分 mechanical / semantic，状态 pass / fail / not_run。全篇语义复核记录 `kind: semantic`、`scope: full_manuscript`、证据文件相对路径、日期与所评 `lecture.md` 的 `output_sha256`。之后任何主稿变化都使旧哈希不再匹配，必须重做受影响检查和全篇复核。完成状态同时要求源文本全部已检查、无 blocking 未决、章全部 reviewed/assembled、主稿与锚点存在、真实的全篇语义 pass 与对应证据。机械通过本身不能授予 complete。

常规检查后最多两轮聚焦返修，`revision_round` 记录 0–2。按规格、方法、阶段衔接、缺失材料、宿主限制分类修正原因。两轮后关键缺陷仍在则 partial 或 needs_input，保留最好稿及下一步，不伪造通过。

## 5. 断点与版本变化

每章结束和每轮检查后保存 `run.json`。其中 `resume.completed/remaining/next_action`、全课计划、术语、源定位、来源及问题必须足以让新上下文继续。用同目录临时文件加原子替换，例如：

```python
from pathlib import Path
import json, os
path = Path(run_directory) / "run.json"
temporary = path.with_suffix(".json.tmp")
with temporary.open("w", encoding="utf-8") as stream:
    json.dump(record, stream, ensure_ascii=False, indent=2)
    stream.write("\n")
    stream.flush()
    os.fsync(stream.fileno())
os.replace(temporary, path)
```

先保存章节再更新记录，避免记录指向尚不存在的内容。`runtime_revision.files` 必须包括 SKILL.md 和实际加载的 refs 的包内相对路径及 SHA-256，不要把模型名称猜成已知事实。`host/model/settings` 只记已知值。

恢复时先读落盘记录并运行检查器，随后读取相应原文及已有章稿。哈希变化返回需重审：保存旧记录与稿件，比较实际变化，列出影响项，将依赖章节置 `needs_review`，使旧全篇复核失效；记录变更理由后才更新输入/runtime 版本。原始快照不能被新的来稿覆盖，更新写新文件。若无法判断影响范围，重审全课结构及所有章，不能只刷新哈希继续。

无变化时从 `resume.next_action` 继续，但仍需核对已有章与待写项，防止重复。完成后必须再次全篇统稿。无文件读写能力时交付文本及真实未完范围，明确无法提供磁盘断点。

## 6. 记录结构速查

[run.schema.json](../schemas/run.schema.json) 是格式说明，`check_run.py` 是显式有限检查器，并非完整 JSON Schema 实现。全部文件路径相对 `run.json`；runtime 文件路径相对 `--repo-root`。外部来源 URI 用于身份记录，不能自动执行。输出到用户指定目录时，以该目录组织运行包或使用允许的相对位置，并将输出文件保存在记录所在运行目录内；需要第二份交付副本时拷贝，记录以可验证原稿为准。

必要字段为 `schema_version/run_id/status/stage/course/inputs/source_review/content_units/sources/chapters/terms/open_issues/runtime_revision/checks/revision_round/output/resume`。新任务不应复制旧 run 的身份、哈希或 pass 记录。可运行 `python3 -m unittest discover -s tests -v` 查看结构夹具和故障行为；它们是工程样本，不是课堂成稿证明。
