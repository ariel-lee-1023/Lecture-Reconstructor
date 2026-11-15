# Completed-recovery checkpoint

Status: complete; stage: deliver; scope: the supplied 21-line synthetic course, with complete prose for three chapters. Main manuscript: lecture.md, SHA-256 `7d8bae4dd4159c369fc7a3f15d730d2875bce374cc917b20b746be9e3125799d`.

Chapter 1's original text and old semantic evidence retain their hashes. The full original run copy is before-resume.json, SHA-256 `3280b7b6ef2398e75f429ca7fab37b3b1b25a93953a299463d1af5832ca70630`. After separately saving chapters 2 and 3 and atomically updating the run, the manuscript was assembled and reviewed in full against the source again. Semantic evidence is checks/full-semantic.md, self-review by the same agent; mechanical results are in checks/resume-final-mechanical.json.

No unwritten chapters or critical defects remain. Two material boundaries remain open: points settlement after timely cancellation and rates for increments other than whole half-hours. The manuscript honestly limits its conclusions without assuming missing rules. Answers beyond this scope require additional rules; current complete status cannot simply be carried over.

Recovery start UTC: 2026-11-15T02:16:39.552799+00:00 (first actual sample; earlier reading occurred before this). Finalized UTC: 2026-11-15T02:24:37.530955+00:00. Exact model ID and settings unknown; the developer description identifies only the GPT-6 family. See resume-audit.json for paths/versions read and backup locations. Real classroom trial, learning outcomes, and independent review: not_run.

For another resumption, run: python3 <isolated-eval>/resume-unchanged/package/scripts/check_run.py <isolated-eval>/resume-unchanged/run/run.json --repo-root <isolated-eval>/resume-unchanged/package --json. Any change to sources, core, or loaded references requires preserving old evidence and assessing impact first, rather than merely updating hashes.
