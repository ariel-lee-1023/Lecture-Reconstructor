# Sources and licensing notice

This project adapts selected methods from the following MIT-licensed skills into methods for producing complete lecture manuscripts. The upstream copyright notice is **Copyright (c) 2026 Ariel Lee**; the full license is retained in [LICENSE](LICENSE). See the [source register](fidelity-ledger/source-manifest.json) for the actual file hashes, Git HEADs, working-tree states, selected scope, and adaptation rationale.

| Upstream repository identifier | Use in this project | Adaptation location |
|---|---|---|
| indwell-via-shared-discern | Discernment of teaching relationships, necessary prerequisites, whole tasks, contrasts, demonstrations, and static dialogue | references/teaching-design.md |
| legal-reasoning-advisor | Grounds for premises and inferences, legal relations, inferential bridges, rebuttals, and conditions | references/law-reasoning.md |
| transcript-proofreader | Contextual repair, entity consistency, uncertainty, and preservation of originals | references/transcript-repair.md |
| Models-and-Machines-colleague | Distinguishing engineering specifications from implementations, integration boundaries, validation layers, and bounded revision | intent.md, spec.md, plan.md; validation design |

These identifiers refer to source repositories supplied locally; unverified remote URLs are not guessed as source addresses. The runtime package does not need upstream access. Authors, titles, and chapter locations are retained in the references. They identify the upstream reference summaries actually read during adaptation, without claiming that the original books were reread in full or independently verified for this project.

`SKILL.md`, the run schema, checkers, recovery workflow, and synthetic tests are this project's implementation. File interfaces and acceptance thresholds are engineering designs, not approaches validated by the original authors. Upstream live interaction, advice-delivery formats, English defaults, and installation or publication authorizations are not inherited.

The MIT license covers this repository's original implementation and adaptations permitted by the applicable licenses. It grants no additional rights to original books, third-party images, complete textbooks, user classroom transcripts, or real case materials. Materials in `evals/cases/` are explicitly labeled synthetic teaching materials created for this project; private inputs and actual user-run outputs are excluded from the publication set by default.
