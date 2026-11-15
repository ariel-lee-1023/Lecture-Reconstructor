# 真实中断与恢复证据

`checkpoint/` 是第一章写完后真实结束的partial断点；`unchanged/`、`input_changed/`、`reference_changed/` 是三个新的生成上下文各自恢复的结果。编排及首检见 [orchestration.json](orchestration.json)。各分支的 `before-resume.json` 与失效记录是合成实验材料，完整临时备份不在公开证据内。

原样分支完成全稿；输入变为17:59到达的分支保留文本内部“撤销失败”矛盾及及时撤销结算规则缺失，状态needs_input；仅reference变化分支完成重审和全稿。检查器通过不消除材料缺口。独立逐源复核见本目录的分支评审文件。

从仓库根目录检查原样与输入变更结果：

```sh
python3 scripts/check_run.py evals/results/resume/unchanged/run/run.json --repo-root .
python3 scripts/check_run.py evals/results/resume/input_changed/run/run.json --repo-root .
```

参考变化分支使用实验性runtime，其workflow末尾多一条复核要求。为了保留仓库唯一运行入口，测试版本保存在ZIP内；先解压到忽略目录，再核对：

```sh
python3 -m zipfile -e evals/results/resume/reference_changed/runtime-fixture.zip .work/reproduce-reference-runtime
python3 scripts/check_run.py evals/results/resume/reference_changed/run/run.json --repo-root .work/reproduce-reference-runtime
```

运行目录里的历史记录保留当时的输入/runtime哈希；对它们使用当前文件重查得到needs_review是预期结果，不能批量刷新旧哈希来“修好”历史。公开元数据中的临时路径已用`<isolated-eval>`代替，主稿和输入字节未改变。
