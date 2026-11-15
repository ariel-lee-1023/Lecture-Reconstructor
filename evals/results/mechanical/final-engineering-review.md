# Final engineering review

Date: 2026-11-15. Review role: independent, read-only engineering review; no participation in this round's A08 generation or independent behavior review. Reviewed spec.md R01–R15, SKILL.md, the four references, run schema, both checkers and their tests, and checked README, NOTICE, LICENSE, the source manifest, and ignore rules.

Conclusion: **1 reproducible P2 engineering defect was identified, repaired by the lead agent, and closed after this reviewer's targeted verification**. This report preserves evidence from discovery and records post-fix results separately. No remaining actual engineering contradiction requiring delivery to be blocked was found. Other independent reviewers handle A08 acceptance; this report does not replace their conclusions.

## Closed P2: a historical whole-manuscript pass incorrectly blocks a revised manuscript that has been reviewed again

- Location: `scripts/check_run.py:358–367`, directly triggered at line 364; related tests are at `tests/test_check_run.py:117–128`.
- Corresponding requirement: R14; `references/reconstruction-workflow.md:49,72` requires invalidating old reviews after manuscript changes, preserving old records and manuscripts, and reviewing again. Checker lines 359–360 explicitly describe checks as an evidence sequence appended over time.
- Trigger: the initial manuscript has a full-manuscript semantic/pass; after modifying the manuscript, retain the old pass and its original hash, then append a new full_manuscript/pass matching the revised manuscript's hash.
- Actual behavior: the checker compares every historical pass with the current manuscript. Although the latest review is valid, the old entry still produces `STALE_REVIEW` and exit code 1. Avoiding this requires deleting, relocating, or rewriting the old entry, contradicting the checker's own account of append-only history.
- Required fix: only the **latest whole-manuscript semantic record** determines whether the current manuscript can be complete. Historical records still undergo checks of their own hash format and evidence files, but their hashes need not equal the new manuscript's hash. A latest stale, fail, or not_run record must still reject complete; a historical pass must not regain authority.
- Suggested regression: old pass + revised manuscript + new pass should succeed; old pass + revised manuscript + latest stale/fail/not_run should fail. A pass for the old manuscript alone must not authorize the modified manuscript.

### Targeted reproduction

Used the synthetic `build_fixture` in `tests/test_check_run.py` to generate files in a system temporary directory. Repository fixtures and real runs were not modified. The complete test suite was not rerun.

1. Call `validate_run` on the original complete fixture: exit code **0**.
2. Add a paragraph to `lecture.md`, retaining the original hash in checks[0].
3. Create a nonempty `review-v2.md` and append checks[1], using the revised manuscript's actual SHA-256 as its `output_sha256`.
4. Call `validate_run` again: exit code **1**; the sole error is `STALE_REVIEW` at `checks[0].output_sha256`.

Key values from the reproduction output:

```json
{
  "baseline_exit_code": 0,
  "old_sha256_preserved": true,
  "latest_review_matches_current": true,
  "result_status": "fail",
  "error_code": "STALE_REVIEW",
  "error_at": "checks[0].output_sha256",
  "result_exit_code": 1
}
```

SHA-256 of `scripts/check_run.py` at discovery: `265ddd2731169446a97f5a863d582a33f5ddd295eba9b5061fe5ddefbb6fb2e5`. Hashes of all reviewed files were saved to a local review backup outside the repository; they are not included in the publication package.

### Targeted post-fix verification

The lead agent modified the checker and regression tests. This reviewer reread `scripts/check_run.py:345–375` and `tests/test_check_run.py:122–134`: the checker first identifies the latest full_manuscript record and binds only that record's pass to the current manuscript hash. Historical passes still have their original hash format and evidence files checked. A subsequent fail/not_run still cannot inherit an old pass.

This reviewer actually ran:

```sh
python3 -B -m unittest discover -s tests -p 'test_check_run.py' -k historical -v
```

Result: **1 targeted test passed, exit code 0**. The case covers both 'retain old hash + new manuscript with a new pass succeeds' and 'latest stale/fail/not_run is rejected.' The complete suite was not repeated. The lead agent separately reported all 40 tests passing; this report does not attribute that full-suite execution to this reviewer.

Post-fix checker SHA-256: `497cd2191e84e7179584762566bbd07bcd2a4768f4b95ef0e28f808f9012fba7`; test-file SHA-256: `d327c9e5613ce8f376545f1cede32959b90c8fb44f6b3ba87a38f245907a647e`. The issue is closed.

## Requirements coverage check

| Requirement | Check result and actual implementation location |
|---|---|
| R01 Self-contained operation | SKILL links four methods inside the package, with no runtime dependency on sibling repositories. Scripts use only the Python standard library, and README specifies Python 3.10+. The text-delivery boundary for hosts without file-writing capabilities is clear. |
| R02–R04 Inputs, clarification, and bounded supplementation | SKILL:12,21–22; reconstruction workflow:7–13,39; transcript repair:7–22 specify nonempty readable input, subtitle preservation, optional materials and core ambiguity, bounded verification, and attribution of source conflicts. |
| R05–R06 Main manuscript and supporting materials | SKILL:8,16,30; reconstruction workflow:25,43; teaching design:25,33 prohibit replacing prose with outlines or advice and require analysis of examples and explanations of questions. Notes and internal records do not replace the manuscript. The run-directory/copy rule in workflow:78 reconciles the specified output location with run-path restrictions. |
| R07 Completion state | The checker explicitly constrains complete status through the stage, nonempty inputs/output, full source-range coverage, unresolved blocking items, chapter states, mapping anchors, current full-manuscript semantic evidence, and resume.remaining. The identified problem was false rejection caused by historical reviews, not unsupported granting of complete status. |
| R08 Content coverage | Reconstruction workflow:11–13,27–37,45 and checker:186–205,241–295 support complete source-range records, five dispositions, locators, acyclic merges, and consistent mappings. Semantic omissions still require rereading the original materials. |
| R09 Transcript repair | The repair module distinguishes restoring input from authorization for subsequent reconstruction, preserves originals, contextual grounds, entity consistency, and consequential ambiguity, and forbids claiming to have listened without audio. |
| R10 Teaching reconstruction | Teaching design specifies learning objects, relationships, prerequisites, whole tasks, variation/invariance, complete demonstrations, and applicability limits. The schema/checker provides corresponding chapter-plan fields. |
| R11–R12 Legal reasoning and sources | Legal reasoning separates premises from inference, and specifies source identity, bridges applying rules to facts, rebuttals, and independent reasons. Historical-law context and Hohfeld/Toulmin limitations are preserved; no excluded legal-source dependency is introduced. |
| R13–R14 Long manuscripts and recovery | Whole-course planning, division by meaning, cross-chapter checks, save order, atomic replacement, impact analysis after input/runtime changes, and re-review of the whole course when impact is unclear are explicit. The checker detects actual hash changes. R14's P2 concerning continuation with historical reviews has been repaired and closed after targeted verification. |
| R15 Instructions in materials | SKILL:26 explicitly states that commands, roles, and earlier authorizations in materials do not change the task or authorize sending messages, installation, or publication. |

## Licensing, sources, and verification boundaries

- LICENSE preserves Ariel Lee's MIT copyright and complete license. NOTICE distinguishes upstream methods, this project's new workflow, and the rights boundaries for third-party books/classroom materials. The four upstream roles were not merged into a complete runtime persona.
- The source manifest records repository-relative identities, actual file hashes, upstream HEAD, worktree state, selected sections, destinations, and adaptation reasons. This round did not reread upstream sources or original books; the review must not be represented as independent verification of the books.
- No local absolute paths or sibling-repository dependencies were found in runtime instructions; `/Users/example/` inside tests is an explicit fault fixture. Ignore rules cover `.work/`, private local inventories, and private runs. No instruction was found treating commands in source materials as authorization for this round.
- The schema describes the format, and both scripts explicitly bound their checks. They check recorded claims and file consistency; they cannot establish that the host actually read references, that legal conclusions are correct, that all substantive meaning is covered, or that learning outcomes occurred. These are stated capability limits, not additional defects.
- The limit of two routine revision rounds is a host-execution requirement; the checker verifies only that revision_round is a nonnegative integer. The specification does not list enforcement of the upper limit among the checker's required bounded constraints, so this difference is not escalated to a separate blocking issue.
- This review did not rerun the full unit suite, evaluate classroom effectiveness, or re-review the extensive historical runs. It did not mark the ongoing A08 work or validation fields awaiting updates as failures.

## Handoff

The lead agent repaired the checker and added regression coverage as described above, and this reviewer completed targeted verification. This reviewer only created and updated this report, without changing the runtime core, scripts, tests, or upstream sources. The lead agent records full mechanical checks and final behavior-acceptance status separately. Discovery evidence and post-fix evidence remain distinct.
