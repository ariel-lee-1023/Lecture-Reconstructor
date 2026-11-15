# lecture-reconstructor — Product intent

Version: engineering baseline v0.1; date: 2026-11-15; status at that baseline: awaiting construction. This document records the confirmed product direction; it does not itself establish that the runtime capabilities have been implemented.

## Why this project exists

Users already have transcripts of university classroom recordings, but the original lectures may contain unclear terminology, missing conceptual relationships, skipped reasoning steps, examples that do not explain the rules, or a confusing sequence. Proofreading can recover what the lecturer said, and summarization can reduce the reading load. Users need a complete, integrated lecture manuscript that corresponds to the original course and improves its teaching quality.

The target users are university students who want to understand and apply course content through a complete manuscript. The first release focuses on law courses, while leaving room in the architecture to extend to other disciplines. The manuscript defaults to the course's language; an explicitly requested manuscript language takes precedence, with necessary original terms retained.

## Product commitment

Given a readable classroom transcript and optional textbooks, slides, and syllabus, reconstruct a complete manuscript that can be read independently and taught directly. Preserve the lecture's substantive content and its correspondence to the course, reorganize the explanation, and supply the necessary background, conceptual relationships, reasoning, case analysis, and transitions.

“Complete” means that the lecture's substantive content receives appropriate treatment. It does not require preserving every spoken repetition or covering the entire discipline exhaustively. “Improvement” must at least make necessary relationships and reasoning clear; greater length or more technical wording alone does not qualify.

The final deliverable cannot be replaced by commentary, editing advice, an outline, or instructions such as “add an explanation here.” Source records and significant corrections are supporting materials, not the main body of the lecture.

## Confirmed architectural decisions

1. Create an independent `lecture-reconstructor` repository. Its first release is a self-contained package of `SKILL.md + references + necessary checking scripts`, executed by a host that can understand text and read and write files. The first release does not implement a separate model API service.
2. `indwell-via-shared-discern` provides the teaching backbone: discern relationships and conditions, connect wholes and parts, and arrange purposeful contrasts and complete demonstrations. Adapt its live interaction mechanisms into methods for writing complete lecture manuscripts.
3. `legal-reasoning-advisor` supplies legal concepts and argumentation methods as needed. Its legal-advice delivery format is not inherited.
4. `transcript-proofreader` supplies optional input repair methods. Its restrictions for faithful records of speech apply only to proofreading and must not prevent course reconstruction that the user has authorized.
5. `prc-legal-sources` is excluded from build dependencies, runtime dependencies, and the source package. A course may use textbooks, slides, and necessary supplementary materials that are actually supplied; investigate specific uncertainties as needed.
6. Feynman, Cognitive, Presentation, Books-to-Skill-Refs, and similar sources are not required dependencies of the first release. Do not prebuild empty adapters for possible future extensions.
7. Models and Machines informs engineering judgment and acceptance design. It is not a persona that must be loaded for every lecture generation.

## Priorities and tradeoffs

Preserve these priorities in order: retain substantive content and important qualifications; maintain reliable source identities and factual statements; explain key relationships and reasoning; make the whole manuscript coherent; make the language fluent.

When these priorities conflict, revise the structure, divide the material into chapters, or retain the necessary explanation. Do not omit exceptions, erase disagreements, or invent evidence to make the manuscript shorter, smoother, or more like a celebrated lecturer's performance. Address the user's explicit length and time constraints instead of silently ignoring them. If they conflict with full coverage, explain the tradeoff and use separate volumes or an accompanying extended manuscript.

## What this release does not do

- It does not perform speech recognition, speaker separation, recording uploads, or audio/video production. Input begins with a transcript.
- It does not build a legal database, update historical lectures to current law by default, or conduct unbounded supplementary research.
- It does not build websites, accounts, payment systems, vector databases, model-provider interfaces, or multi-agent orchestration platforms.
- It does not require the user to answer quiz questions, complete a learner profile, or finish exercises before receiving the manuscript.
- It does not promise accurate examination predictions or treat a lecturer's emphasis as a general legal conclusion.
- It does not generate slides, Word files, PDFs, or interactive HTML by default. The standard first-release deliverable is a Markdown manuscript. Existing host export capabilities may be used separately at the user's request.
- It does not modify upstream repositories, install globally, commit, push, or publish by default. Earlier authorizations in upstream documents do not expand this project's authorization.
- It does not claim demonstrated learning outcomes, zero errors, or superiority to all teachers.

## How to determine whether the project has succeeded

Three conclusions must remain distinct:

| Layer | Evidence | What it establishes |
|---|---|---|
| Repository and records are usable | Checks of files, paths, structured records, and loading in isolation | The engineering package has the correct structure, and the checkers can detect the defined mechanical errors |
| Actual generation behavior meets the specification | Actual inputs, complete generated outputs, and independent review against the original materials | The tested scenarios produced manuscripts that meet the requirements, rather than merely well-written instructions |
| Learning outcomes improve | Actual learners' explanations, judgments on varied cases, or delayed performance | The corresponding effects occurred under the tested conditions; the first two layers cannot substitute for this evidence |

Follow `spec.md` for first-release construction and behavioral acceptance. Without real classroom samples, the repository can still be completed and synthetic scenarios validated. Record real classroom trials and learning outcomes explicitly as `not_run`.

If all file checks pass but the output still consists of textbook summaries or editing advice, revise the task contract or teaching methods. If combining stages under the same specification causes omissions, duplication, or confusion about source identities, inspect the stage interfaces and review of the whole manuscript. These are engineering applications of Models and Machines methods in this project, not effectiveness conclusions already established by the sources.

## Document relationships and changes

This document defines purpose and boundaries; `spec.md` defines behavior and acceptance; `plan.md` defines the order of implementation, testing, and recovery. If they conflict, prioritize the user's explicit requirements and update the documents together, rather than silently choosing one to follow. During implementation, organizational details may change without changing the purpose. Before expanding the first-release scope, identify the new requirement and its cost.
