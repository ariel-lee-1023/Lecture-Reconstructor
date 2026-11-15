# lecture-reconstructor — Implementation Plan

Version: v0.1; date: 2026-11-15; status: the build baseline and synthetic acceptance have been executed; see the final sections for the subsequent language-policy change and English translation. Evidence for completed checklist items is in [validation.md](fidelity-ledger/validation.md) and [A01–A12](evals/acceptance.md).

## 1. Delivery structure and responsibilities

Preserve the existing `intent.md`, `spec.md`, and `plan.md` as the requirements baseline. Make the minimum product work first, then complete acceptance testing; do not build a platform first.

```text
lecture-reconstructor/
├── intent.md
├── spec.md
├── plan.md
├── SKILL.md                         # Sole runtime entry point
├── AGENTS.md                        # Repository maintenance rules
├── README.md                        # Inputs, outputs, usage, and actual validation status
├── LICENSE
├── NOTICE.md
├── .gitignore
├── references/
│   ├── teaching-design.md           # indwell adaptation for manuscript design
│   ├── law-reasoning.md             # Legal explanation and argument
│   ├── transcript-repair.md         # Optional input repair
│   └── reconstruction-workflow.md   # New coverage, long-form, source, and recovery workflow
├── schemas/run.schema.json
├── scripts/
│   ├── validate_repo.py
│   └── check_run.py
├── evals/
│   ├── cases/                       # Substantive synthetic scenarios and fixtures
│   └── acceptance.md                # A01–A12 inputs, expectations, and review methods
└── fidelity-ledger/
    ├── source-manifest.json         # Publishable upstream provenance and adaptation records
    └── validation.md                # Actual checks, behavior, pilot status, and defects
```

This is the structure specified for the build; creating empty files does not satisfy delivery. `.work/` holds private run materials and is ignored by default. UI metadata, global installation, upstream symlinks, and additional frameworks are unnecessary. Add a relative discovery entry pointing to this repository's sole core only if the host actually requires one.

`BUILD.md` and `source-inventory.local.json` are the build handoff materials: the former guides the builder, and the latter records local sources. Remove local records from version control when preparing publication. The public manifest must not contain personal absolute paths.

## 2. Integrating and adapting existing files

See `source-inventory.local.json` for source roots and the file versions used for this build. Paths below are relative to each source repository. **All adaptations take place in the new repository; original upstream files remain unchanged.** Do not concatenate several complete SKILL files or copy historical maintenance ledgers in bulk.

| Source | New file and adaptation | Explicitly not inherited |
|---|---|---|
| Teaching choices, contrasts, whole tasks, and precise expression in `indwell-via-shared-discern/SKILL.md`; `references/reference-marton-booth-awareness.md`, `reference-ambrose-learning.md`, `reference-van-merrienboer-complex.md` | Adapt into `teaching-design.md`: identify the relations a section should make discernible, supply prerequisites, start from the whole problem, and provide complete demonstrations and purposeful variation. Preserve authors, titles, chapter locations, and applicability conditions. | Diagnoses that require observing learner responses, interaction loops that repeatedly wait for user participation, or certification of competence or learning outcomes |
| `reference-alexander-dialogic.md` and `reference-multimedia-handbook.md` in the same repository | Add sections loaded as needed in the same file: address real questions in the material, respond to objections, preserve disagreements, and use parallel comparisons and necessary text/visual explanations. Explain the limitations of adapting these methods to a static manuscript. | Invented student participation, mandatory HTML/SVG production, or treating visual polish as evidence of understanding |
| `legal-reasoning-advisor/SKILL.md`; `references/move-taxonomy.md`, `reference-toulmin-uses-of-argument.md`, `hohfeld-toolkit.md`, `reference-maccormick-rhetoric.md` | Adapt into `law-reasoning.md`: distinguish inference from the grounds for premises, clarify legal relations, implicit bridges, rebuttals, and conditions, and turn these into explanation methods that can be written directly into a course. | Legal-advice responses as the default deliverable, a mandatory framework for every topic, universalizing historical common-law material, or capabilities of a current-law database |
| Contextual repair, entity memory, uncertainty, and original preservation in `transcript-proofreader/SKILL.md` | Adapt into `transcript-repair.md` as a preliminary operation when needed. | An English default, editorial notes as the main deliverable, mandatory Word/PDF, specialized lists of people's names, or extending the prohibition on reordering into reconstruction |
| Newly written, incorporating interface boundaries from the methods above | `reconstruction-workflow.md`: read the whole course first, establish content items and sources, plan, write chapters, reconcile the whole manuscript, review coverage, revise, and save checkpoints. | Diagnostic reports that simply hand the work back to the user, or multi-role reviews with no responsibility for producing a manuscript |
| Newly written | `SKILL.md`: task and input/output contract, necessary rules, and routing to four references as needed; explicitly default to complete prose. | Entire upstream personas, duplicated full sets of book summaries, or unrelated maintenance instructions |
| `Models-and-Machines-colleague/SKILL.md`; the Brooks Design and MacKenzie Proof references | Use only as design grounds for these three engineering documents and the separation of validation layers; register provenance in the engineering section. | Inserting M1–M5 or philosophical persona analysis into every lecture |

Adapted references must be self-contained; merely saying “see the file in the sibling repository” is insufficient. Preserve the key mechanism, its boundaries, an example that makes the method distinguishable, and the original source location. Do not distill whole books again. Separate original source propositions from this project's new design for manuscript production; do not attribute the new workflow to the original authors.

At the build baseline, all three principal sources carried the MIT license and `Copyright (c) 2026 Ariel Lee`. Verify the actual files during construction, retain license terms and attribution, and list adaptation sources in `NOTICE.md`. Do not extend that license to source books, third-party images, complete textbooks, or original classroom materials.

## 3. Phase 0: Confirm scope, inventory, and backups

- [x] Read the three requirements documents and `BUILD.md`; confirm that the first release is a skill repository and excludes `prc-legal-sources`.
- [x] Check whether the target directory exists and record its file list and Git status, including untracked files. Do not assume it is empty or already uses Git.
- [x] Create a timestamped backup directory outside the target. Back up each existing file to be modified and record its relative path and SHA-256. If it did not exist, record it as newly created in this round.
- [x] Preserve existing user changes and make local edits where possible. Ask the user to decide only when a real conflict cannot be resolved while preserving their work. Do not automatically stash, run `reset --hard` or `clean -fd`, or replace the entire directory.
- [x] Maintain a local change list with every written path, its hash before the write, and the hash after the builder's latest write, for recovery and concurrent-change detection. Reading upstream files does not require committing to or modifying upstream repositories.

Exit condition: the files to modify, the new files, and the recovery locations for existing content are known. Source and target repository boundaries are clear.

## 4. Phase 1: Fix the actual source versions and minimum core

- [x] Recheck file existence and SHA-256 against the local source inventory. If they differ from the engineering package's records, read the differences and choose and record the version actually used; do not automatically overwrite upstream files.
- [x] Record the source repository, available HEAD, relative source path, actual hash, worktree modification status, extracted sections/ranges, target file, and adaptation rationale. A hash establishes content identity, not correctness.
- [x] Write `SKILL.md` and `AGENTS.md`. The former governs manuscript production; the latter governs only this project's maintenance and source handling. Remove implicit English defaults, interaction that blocks delivery, and inherited publication authorization.
- [x] Adapt the four references according to the mapping, using narrowly scoped loading as needed. Complete `teaching-design.md` and `reconstruction-workflow.md` as the backbone first, then integrate legal methods and optional proofreading.
- [x] Add the actual LICENSE, NOTICE, and ignore rules, and save the source manifest. Use repository identifiers and relative paths in the manifest.

Exit condition: the core can locate the necessary methods without any sibling repository, and the direct output expected from reading a transcript is explicit. At this point, actually generate a draft from one small synthetic input to confirm that the task has not collapsed into commentary, then proceed to record engineering.

## 5. Phase 2: Internal records, long manuscripts, and mechanical checks

- [x] Define `run.schema.json` according to R08 and R12–R14. Retain only fields actually needed for continuation, provenance, and acceptance.
- [x] Explain in `reconstruction-workflow.md` how stage outputs connect and how source content maps to manuscript locations after reordering.
- [x] Implement `validate_repo.py` and `check_run.py`. The former checks package structure; the latter checks bounded mechanical constraints for a run. Neither may claim to verify teaching quality or legal correctness.
- [x] Create a valid record and a small set of faulty variants, actually execute the checkers, and verify exit codes and actionable error locations. Cover the specification's dangling references, merge cycles, out-of-bounds ranges, missing anchors in completed chapters, changed input/runtime hashes, and missing or stale whole-manuscript semantic reviews. Valid `planned` chapters may pass.
- [x] Check that interruption records are sufficient to resume a long manuscript: source hashes, read/unread ranges, the whole-course plan, terminology, chapters and their states, sources, unresolved issues, and the next action.

Exit condition: checkers identify specific structural errors and accept valid examples. A fabricated claim of completion based only on a status field is rejected. Runtime semantics still require actual generation and review.

## 6. Phase 3: Actual behavior validation

- [x] Create substantive A01–A12 test inputs. Prefer reusing a small set of materials across scenarios; deliberately easy-to-miss items must actually appear in the original material.
- [x] When no real classroom material is supplied, use concept, case, and disagreement lectures clearly labeled as synthetic. Supply sufficient rules and facts; do not present them as current law, real precedents, or real teaching records.
- [x] Generate actual manuscripts in isolated run directories. Save inputs, outputs, the core version, actual model information, and reviews; label unknown settings `unknown`.
- [x] Have a reviewer who did not participate in that generation compare the original material and manuscript, focusing on easily omitted content, decisive conditions, reasoning, and source identity. Do not merely ask whether the writing is good.
- [x] For A08, actually pause at the end of a chapter and resume in a fresh context using only saved records. Separately test invalidation and re-review after an input change, and after a reference change with the original input unchanged.
- [x] For A10, copy the entire new repository to an isolated location and restrict the evaluator to reading that package and the test materials. Actually generate a manuscript to test self-sufficiency.
- [x] Generate a plain direct-rewriting baseline and a new-skill version for each of the three sample types, record configuration and resource differences, and compare them anonymously. Record and analyze any lack of advantage honestly; do not change scores to obtain a pass.

Exit condition: each of A01–A12 has a `pass/fail/not_run` status and evidence. The builder may deliver a version awaiting acceptance, but must not mark unrun tests as passed. If model execution is unavailable, complete the feasible engineering work and identify behavior acceptance as the specific blocked part.

## 7. Phase 4: Bounded revision and delivery

- [x] Classify failures as specification, method, stage-composition, missing-material, or host-limit issues. Fix the part that actually caused the failure.
- [x] Default to at most two focused revision rounds, rerunning affected scenarios and necessary mechanical checks. A substantial change to the shared core requires rerunning all relevant behavior scenarios.
- [x] Keep unresolved critical defects marked as failures; exhausting the revision budget does not establish completion. Preserve the best usable manuscript, reproduction materials, and the next action.
- [x] Write the README: purpose, minimum input, main output, usage examples, runtime boundaries, and actual validation status. Do not claim that installation, publication, or learning outcomes have been verified.
- [x] Check runtime files for local absolute paths, missing relative references, or excluded dependencies. Check that original classroom materials, textbooks, temporary runs, and backups are outside the publication set.
- [x] Use this round's file hashes to confirm that upstream files were not modified by this work. If an external process changed a source file concurrently, record and investigate it; do not restore someone else's changes without authorization.
- [x] Hand over the directory, invocation method, three validation layers, unresolved defects, and recovery locations. Global installation, commits, pushes, creation of a remote repository, and public publication require separate user authorization.

Exit condition: engineering artifacts can be handed over, and status claims match the evidence. Repository construction, behavior acceptance, a real classroom pilot, and learning outcomes must not be conflated into “everything is complete.”

## 8. Recovery and failure handling

| Event | Recovery action |
|---|---|
| A target file was damaged by an edit | Restore from the baseline only if the current hash matches the builder's latest written version. If it was changed concurrently, preserve both versions and restore locally without overwriting someone else's new changes. Verify the result and retain the diff. |
| A newly created file must be withdrawn | Move it to an isolated directory solely on the basis of the change list; delete it only after confirming that it belongs to this round. |
| Upstream changed | Do not automatically refresh all knowledge. Read the actual diff, update the selected scope and manifest, and rerun affected scenarios. |
| A long manuscript stops midway | Save completed chapters and status. On the next run, verify input/core hashes and continue from unfinished items. |
| Original input or the core/reference changes | Locate affected content and dependent chapters, and mark them for re-review. Preserve old manuscripts and version records. If the impact is unclear, recheck the whole-course structure. |
| Two revision rounds do not resolve the problem | Preserve the manuscript and defect evidence, and deliver an explicit state requiring further repair. Do not retry indefinitely. |
| Optional web access or document parsing is unavailable | Use materials already obtained and preserve uncertainty. Request supplementary input only when the gap affects the core task. |

Do not roll back upstream repositories, delete the user's existing files, or replace an entire directory to solve a single-file problem. Preserve failed outputs and review records in private run directories for reproduction, not for publication by default.

## 9. Requirements traceability and final engineering checklist

| Requirement | Main implementation location | Validation |
|---|---|---|
| R01–R04 | SKILL, reconstruction-workflow, README | A07, A10, A12 |
| R05–R07 | SKILL, reconstruction-workflow, run schema | A01, A11, status fault fixtures |
| R08–R09 | transcript-repair, content records, and checkers | A02, A04, range and mapping fixtures |
| R10–R12 | teaching-design, law-reasoning, source records | A03, A05, A06 |
| R13–R14 | reconstruction-workflow, run schema, checkers | A08, input and reference change branches |
| R15 | SKILL, AGENTS | A09 |

- [x] The core and four references contain substantive content, have clear responsibilities, and do not duplicate entire personas.
- [x] The main deliverable is an actual complete lecture manuscript; sources and editorial comments do not displace the prose.
- [x] The minimum input is sufficient to work, while legal boundaries and the identities of disputed positions are preserved correctly.
- [x] Checkers have been executed, and their semantic limitations are explicit.
- [x] Behavior tests have actual artifacts, with unrun items and defects marked honestly.
- [x] Sources, adaptations, licenses, and upstream versions are traceable; original classes and textbooks are not public by default.
- [x] Long manuscripts can be interrupted and resumed, and receive whole-manuscript reconciliation rather than mechanical concatenation of sections.
- [x] Backups and recovery operate at file level; existing repositories were not modified by this project.

## Historical build notes (2026-11-15)

The core, references, checkers, and fixtures were implemented in parallel by responsibility, then integrated with actual behavior validation; this was not a strictly sequential pipeline. The first three lecture generations encountered a schema that had not yet been copied; the incident record was preserved, and the final A10 was run independently with the complete package. Forty mechanical tests passed, and all A01–A12 synthetic behavior cases had evidence. The input-change branch preserved the material conflict and `needs_input`; the real classroom pilot and learning outcomes were both `not_run`. Two comparison categories were broadly comparable, while the disagreement lecture was locally stronger and resource use differed; no general improvement was claimed. The final engineering review's erroneous rejection of historical review hashes was fixed, and bounded path detection was completed. No identified critical engineering defects remained. At the end of that initial build, Git had only been initialized; no commit, push, installation, or public publication had yet occurred.

## User-requested language-policy revision (2026-11-15)

The manuscript language rule changed to prioritize an explicitly requested output language, otherwise using the course language; the request message's language does not automatically switch the output language. SKILL, README, intent, spec, and transcript-repair guidance were updated together. BUILD retains the original handoff text and identifies the current rule. Checkers and schema were unchanged. That revision ran only format, package-structure, and rule-consistency checks; it added no low-impact wording tests and did not reassign historical A01–A12 results as behavior passes for the revised core. Historical requests that explicitly specified Chinese and their run hashes were preserved unchanged.

## English documentation and runtime translation (2026-11-15)

At the user's request, `SKILL.md`, `intent.md`, `spec.md`, `plan.md`, `AGENTS.md`, and all four method references were translated into English. Requirement and acceptance IDs, source attribution and locators, method boundaries, record fields, paths, and commands were retained. The synthetic repair example received an explicitly identified English adaptation. English documentation does not set an English manuscript default: an explicit output-language request still takes precedence, otherwise the course language applies.

This translation changes model instructions, so it has a distinct runtime identity. The previous runtime and validation records are preserved in [runtime-revision.pre-english-core.json](fidelity-ledger/runtime-revision.pre-english-core.json) and [validation.pre-english-core.json](fidelity-ledger/validation.pre-english-core.json). Historical evaluation inputs, outputs, and hashes remain unchanged. Textual equivalence review and mechanical checks do not establish behavioral equivalence; model behavior for the English runtime remains `not_run`, as do real classroom trials and learning outcomes.

## Repository-wide English translation (2026-11-15)

The remaining tracked documentation, provenance records, fixtures, historical manuscripts and reviews, checker messages, test prose, and archived runtime members were translated into English at the user's request. Historical original bytes remain in Git at commit `b0390af4a584b884a62dba6aba7994514df81c8d`; the [translation manifest](fidelity-ledger/english-translation-manifest.json) records their identities and those of the English copies. Historical hashes and acceptance results were not reassigned to the translations. Current model behavior, classroom trials, and learning outcomes remain `not_run`. The course-language selection policy and the five runtime instruction files were unchanged in this pass. Functional multilingual detection and its regression inputs retain their original values through Unicode escapes.
