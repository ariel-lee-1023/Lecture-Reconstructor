# Evidence of actual interruption and recovery

`checkpoint/` is the actual partial checkpoint where generation ended after chapter 1. `unchanged/`, `input_changed/`, and `reference_changed/` contain recovery results from three fresh generation contexts. See [orchestration.json](orchestration.json) for orchestration and initial checks. Each branch's `before-resume.json` and invalidation records are synthetic experimental material; complete temporary backups are not included in public evidence.

The unchanged branch completed the manuscript. The branch with receipt changed to 17:59 retained the internal contradiction 'cancellation failed' and the absence of timely-cancellation settlement rules, with status needs_input. The reference-only-change branch completed re-review and the manuscript. A checker pass does not remove gaps in the materials. See the branch review files in this directory for independent source-by-source verification.

Check the unchanged and input-changed results from the repository root:

```sh
python3 scripts/check_run.py evals/results/resume/unchanged/run/run.json --repo-root .
python3 scripts/check_run.py evals/results/resume/input_changed/run/run.json --repo-root .
```

The reference-changed branch uses an experimental runtime with one additional review requirement at the end of its workflow. To preserve the repository's sole runtime entry point, that test version is stored in a ZIP. Extract it into an ignored directory before checking:

```sh
python3 -m zipfile -e evals/results/resume/reference_changed/runtime-fixture.zip .work/reproduce-reference-runtime
python3 scripts/check_run.py evals/results/resume/reference_changed/run/run.json --repo-root .work/reproduce-reference-runtime
```

Historical records in run directories retain their input/runtime hashes from the time of execution. Rechecking them against current files is expected to produce needs_review; do not bulk-refresh old hashes to 'fix' history. Temporary paths in public metadata have been replaced with `<isolated-eval>`; manuscript and input bytes were unchanged.
