# Whole-Course Reconstruction, Records, and Recovery

This file defines a production workflow newly designed for this project. The teaching principles in the sources do not automatically imply these file formats, stages, or quality thresholds. The workflow serves a complete lecture manuscript; chapters may follow the material's needs, and readers do not need to see engineering fields.

## 1. Input and boundaries: ingest → map

Create `.work/runs/<run-id>/` for the task. For a single transcript, save the original as `input/original.*` and normalized text as `input/transcript.txt`. With several inputs, give each original and its normalized text distinct paths under `input/`. Record both hashes for each. Save a snapshot of pasted text as well. Normalization addresses only encoding, subtitle structure, and necessary readability; it must not remove important text. Preserve timestamp text for traceability without guessing missing times. Each `inputs` entry uses `path` and `sha256` for the original file, and `normalized_path` and `normalized_sha256` for the text actually used to establish line locations. Identical text may use the same path.

First establish what can actually carry the lesson. A substantial transcript may provide both problem and evidence. A weak transcript may preserve useful facts but miss their significance. A clause, judgment, literary passage, or dataset may support an entire redesigned session when the transcript is absent or empty. Record the basis in `course.scope` or `course.assumptions` and the document's identity in `inputs.kind`. Preserve any useful classroom evidence and describe a new design as a lecture built from the document. If an optional file is empty, log that gap without putting an empty placeholder into the required coverage set. If there is no usable basis after checking what is available, record `needs_input` and ask for the specific material that could unlock the lesson. Missing textbooks, learner profiles, or similar optional material do not block work. Record an unknown course jurisdiction or period as `unknown`; put retractable assumptions in `course.assumptions`. When an important meaning is unclear, ask only the smallest question that changes the judgment, and preserve the other content that can be processed.

For a packet, establish what each part can tell you and which class it belongs to. Use the existing input identity, source locator, and course scope fields. If one export contains an automatic recap, edited notes, and timestamped speech, locate each by section. Use the speech for what was said, including self-corrections and limits. A recap may help find a passage. Its repetition adds no independent support. A slide can establish its own wording or illustration. Determine from the lecture whether the speaker used it, amended it, or deferred it. Connect overlapping recordings by shared passages and topic changes. A date or filename alone is a weak basis for assigning material to a particular lecture.

For a reference such as “the lower line here,” find the cited figure, table, passage, or board work if it is available. Where layout carries the meaning, inspect the original page, column headings, labels, or legend before using the extracted text. Retain the page or slide number alongside any normalized lines. Describe the relevant feature in the prose. If the exhibit is missing, preserve what the spoken explanation establishes and qualify the specific inference that needs the exhibit. Register the texts that carry the lesson, including a source document when it substitutes for an absent transcript, and other materials the user asks to have fully covered as `inputs` for line-range review. When only a passage of an optional reading supports an added point, register that passage in `sources` with its actual locator and read status. Preserve the full scope of any material the user expressly asked to cover.

After reading the material in scope, use `source_review` to record one-based, inclusive `start_line/end_line` ranges and `reviewed/unread` status for each input's normalized text. These fields record reading, not proof of understanding. A database item is not required for every sentence, but all input lines should have coverage records. Titles and subtitle lines outside the main prose must not leave gaps that are mistakenly treated as unread.

Divide `content_units` by actual meaning: definitions, propositions, reasoning, cases, exceptions, counterexamples, substantive questions, and the teacher's examination advice. Save a stable ID, a brief proposition, input line ranges and a short excerpt, and the type for each item. Pending items before reconstruction may be `unresolved`; explain that they have not yet been written and assess whether they are blocking. Do not present them as complete. A page title or chapter anchor records a location. If dropping one condition, number, objection, or exception would change what a reader concludes, give it a distinct proposition or name it explicitly in the existing item. Overlapping sources can share a proposition and retain their separate locators. Do not multiply entries for repeated headers or count an agenda heading as teaching.

When recognition damage matters, examine the entire turn and how later passages reuse the term. Compare the observed form with plausible alternatives on sound, syntax, referent and the actions attributed to it. A clearer source can confirm spelling without confirming who said which words. Distinguish an actual audio check, a speaker correction, and a contextual inference. An intelligible but false assertion belongs to the subsequent reasoning stage. Keep its original meaning visible in the record when the lecture corrects it.

## 2. Teaching plan: plan

Before selecting chapter titles, test the best available example. Write down two live answers, the detail that might distinguish them, and what else would have to be read to decide. When the teacher's example fails, retain the facts and separate three possibilities: an omitted premise saves the conclusion, a more limited conclusion survives, or the conclusion must change. Choose the one supported by the actual document. A disputed interpretation can become the organizing question of a lesson. If the teacher merely named a text, read the relevant complete unit and its context, and let the original text govern what you can teach.

A compact example of source-led redesign: a fictional seminar packet says only “the notice deadline matters.” Clause 4 of its exhibit ends a claim unless notice **reaches** the buyer by Friday, while clause 9 treats dispatch as sufficient for **routine correspondence**. A courier took the packet on Friday and delivered it on Monday. A lecture that merely warns students to watch deadlines misses the problem twice. First, ask what kind of notice the parties sent. For a claim, clause 4 specifies receipt. For routine correspondence, clause 9 gives dispatch a different effect. Then apply each rule to the actual pair of dates. If the packet never identifies which notice was sent, teach both consequences and leave that particular result open. A reader can now identify the fact that changes the answer. The example and teaching sequence in this paragraph are project illustrations.

For a weak explanation that announces only the accepted answer, make the alternative intelligible before rejecting it. Identify why it works on the easy example and construct or select the nearest supported case on which the answers diverge. Spell out the decisive step and, where it serves the lesson, work a variant that changes a relevant condition while keeping the rest fixed. If the obstacle is choosing a method, an additional example with the method already named cannot demonstrate that choice. Never ascribe a misconception to an actual student without evidence.

Establish the whole-course problem, chapter order, and glossary before writing individual chapters. For each chapter, record `learning_object`, `relations`, `prerequisites`, `approach`, `role`, and `content_unit_ids`. For example, the learning object is “the distinction between consent and a claim-right,” and the relation is “freedom from improper interference does not mean that another party owes a performance.” Contrast changes in authorization and promises within the same borrowing situation. For how to explain these in the prose, see [Teaching design](references/reference-teaching-design.md).

Preserve boundaries that matter to the user's deliverable. For consecutive classes, establish what each one taught, which example carries over, and what question remains for the next. A course pack can include material that was never reached in class. Include that material as a separately identified development only when it serves the requested scope. If the user asks for separate lectures, make each readable independently and map it back to the appropriate portion of the packet.

Use stable chapter IDs and explicit HTML anchors, such as `<a id="ch-consent"></a>`; detailed items may point to section anchors. A typical chapter path is `chapters/01-consent.md`. A `planned` chapter may lack a file and anchor; once prose is written, verify that they actually exist. Changing chapter order does not change IDs. Record terminology decisions in `terms`, and do not randomly substitute synonyms for the same entity.

Divide long courses at complete conceptual or argumentative units. Add connections to preceding or subsequent classes only when those materials actually exist. If the target length cannot accommodate substantive content, preserve the full scope and explicitly use separate volumes or a complete companion manuscript, or ask for a decisive scope choice. Do not conceal omissions behind a “condensed version.”

## 3. Writing and sources: draft

Write explanatory paragraphs that can be read aloud directly, chapter by chapter. Do not output suggestions for someone else to complete. The opening establishes the course problem, the ending fulfills the learning object, and chapter transitions explain how the current step serves the whole course. Analyze the facts, changed conditions, and unchanged factors in examples; provide complete explanations for learning questions.

Use only the following content-item treatment states:

| State | Record and manuscript responsibility |
|---|---|
| represented | Explained; `targets` points to a chapter ID and a real anchor. |
| merged | Combined with another item; retain the original location, point `merge_into` to the destination content ID, and use `targets` for the actual prose. Cycles are prohibited. |
| corrected | Save `original_meaning`, the reason for the change, and `correction_basis`; associate `source_ids` with grounds actually read, and point to the corrected prose. |
| excluded | Give a specific reason, such as irrelevance to the course or pure repetition. Do not exclude substantive content because it is difficult, lengthy, or disputed. |
| unresolved | Provide `blocking` and `blocking_reason`; if the issue changes the core argument, it must prevent complete status. |

`locations` retains original course locations; `targets` records manuscript locations after reordering. Important new propositions may become new explanatory items linked to actual input or supplementary sources, but must not have invented original line numbers. Purely supplementary items with no original course location use empty `locations`, real `source_ids`, and an explicit identity as added material.

`sources` records the ID, actual path or URL, version, precise location, and `read_status`. The original course input may also be registered as a source. Precise legal facts and attribution of scholarly positions require support that has been read. Label teaching assumptions as assumptions, and explain which premises support explanatory inferences. Preserve jurisdiction, time, conditions, and attribution in the prose wherever they affect the conclusion; put detailed audit notes in `notes.md`. Opening a link does not establish support for a proposition.

## 4. Chapter checks and whole-manuscript review: review → assemble → deliver

When a chapter is finished, write its file before changing `chapters.status` to `drafted`. After checking omissions and reasoning, change it to `reviewed`; use `needs_review` when re-review is required, and provide `missing_reason` if its file is absent. Reconcile the whole manuscript for repeated definitions, contradictions, drifting terminology, unfulfilled setup, and abrupt transitions. Assemble it into `lecture.md` while retaining target anchors.

Semantic review must compare the actual input with the actual main manuscript again, paying particular attention to small cases, objections, examination advice, negations, and exceptions that the content list itself might have missed. Check the source identity of every important added fact, whether reasoning is complete, and whether contrasts explain the decisive conditions. Test a difficult or consequential passage in both directions. Starting at the source, find the sentence in the finished manuscript that explains the hinge in the argument, including the exception or objection. Starting at the manuscript, check the source for its parties, numbers, qualifiers, quotation, or other premise on which the conclusion rests. Record the input locator, output passage, and what the comparison found, including any repair. Matching titles, page counts, or chapter anchors alone do not demonstrate this. An independent reviewer may be used, but praise based only on reading the manuscript cannot replace comparison. Record what is known about the reviewer's identity, the method, item-level evidence, and defects; use `unknown` for unknown settings.

First run `python3 scripts/check_run.py .work/runs/<run-id>/run.json --repo-root .`. Exit code 0 means structural checks passed, 1 means a record or file error, and 2 means that input/runtime changes require re-review. The script does not judge legal or teaching correctness for you and does not change status automatically.

`checks` distinguishes mechanical / semantic checks, with pass / fail / not_run status. A whole-manuscript semantic review records `kind: semantic`, `scope: full_manuscript`, the evidence file's relative path, the date, and the `output_sha256` of the reviewed `lecture.md`. Any subsequent change to the main manuscript makes the old hash no longer match; rerun affected checks and the whole-manuscript review. Complete status also requires that all source text has been reviewed, no blocking issue remains unresolved, all chapters are reviewed/assembled, the main manuscript and anchors exist, and an actual full-manuscript semantic pass has corresponding evidence. A mechanical pass alone cannot confer complete status.

After routine checks, allow at most two focused revision rounds; `revision_round` records 0–2. Classify the reason for each correction as specification, method, stage integration, missing material, or host limits. If critical defects remain after two rounds, use partial or needs_input, preserve the best manuscript and next action, and do not fabricate a pass.

### A source-to-manuscript check, worked from beginning to end

This synthetic seminar uses an invented library rule. The student needs to distinguish the event that stops a fee from the evidence available to prove its time.

| Supplied passage | What it can establish |
|---|---|
| Transcript, lines 1–2: the instructor starts to say “when the assistant scans it,” then corrects herself: the fee stops when the book goes into the return box. | The correction identifies the operative event. Retain both events because the lecture asks students to distinguish them. |
| Transcript, lines 3–4: the box closes at 18:00. A witness saw the book enter at 17:58. Staff scanned it at 18:06. A student asks whether the late scan changes the fee. | The case supplies a deadline, two times, a witness, and an objection. Each matters to the answer. |
| Slide 3: the receipt displays the staff scan time. An automatic recap of the class says the fee runs until scanning. | The slide identifies what the receipt measures. The derivative recap conflicts with the teacher's explicit correction. |

One suitable manuscript passage reads: “The fee stops at deposit. Here the witness saw the book enter the box at 17:58, before it closed. The 18:06 receipt tells us when the staff scanned it. A scan eight minutes later cannot make this deposit late. Suppose instead that all we had was that receipt. We could establish that staff had the book by 18:06. On that evidence alone we could not decide which side of 18:00 the deposit fell on.” The last two sentences introduce a teaching variation. They change the evidence available without changing the rule or inventing a new event in the original case.

In the record, the rule, the original case, and the student's objection retain their transcript locators. The slide supports the separate proposition about what a receipt records. They can all point to the same passage if it actually explains each point. The misleading recap gets its own source identity and a brief reconciliation where consequential. Do not mark the teacher's final rule as a factual correction by the author of the manuscript: she corrected her own false start. If an earlier draft had said the scan stopped the fee, revising that draft repairs a reconstruction error. To review, start at the student's question and find its answer in the paragraph. Then start at the paragraph's final sentence and check that it is conditional on removal of the witness evidence. These two comparisons detect different errors even when every chapter link is valid.

## 5. Checkpoints and version changes

Save `run.json` at the end of each chapter and after each review round. Its `resume.completed/remaining/next_action`, whole-course plan, terminology, source locations, sources, and issues must be sufficient for a fresh context to continue. Use a temporary file in the same directory followed by atomic replacement, for example:

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

Save chapters before updating the record, so that it does not point to content that does not yet exist. `runtime_revision.files` must include package-relative paths and SHA-256 hashes for SKILL.md and the references actually loaded. Do not present a guessed model name as known fact. Record only known values in `host/model/settings`.

To resume, first read the saved record and run the checker, then read the relevant original text and existing chapter manuscripts. A changed hash requires re-review: preserve old records and manuscripts, compare actual changes, list affected items, set dependent chapters to `needs_review`, and invalidate the old whole-manuscript review. Update input/runtime versions only after recording the reason for the change. New input must not overwrite the original snapshot; write updates to new files. If the scope of impact is unclear, review the whole-course structure and all chapters again. Do not merely refresh hashes and continue.

When nothing has changed, continue from `resume.next_action`, while still checking existing chapters against pending items to prevent duplication. Reconcile the whole manuscript again before completion. Without file-reading/writing capabilities, deliver text and an honest account of unfinished scope, explicitly stating that a disk checkpoint cannot be provided.

## 6. Record structure quick reference

[run.schema.json](schemas/run.schema.json) describes the format. `check_run.py` is an explicit, bounded checker, not a complete JSON Schema implementation. All file paths are relative to `run.json`; runtime file paths are relative to `--repo-root`. External source URIs record identity and must not execute automatically. When delivering to a user-specified directory, organize the run package there or use permitted relative locations, and keep output files within the run directory containing the record. Copy a second delivery version if needed; the record must refer to the verifiable original manuscript.

Required fields are `schema_version/run_id/status/stage/course/inputs/source_review/content_units/sources/chapters/terms/open_issues/runtime_revision/checks/revision_round/output/resume`. A new task must not copy an old run's identity, hashes, or pass records. You may run `python3 -m unittest discover -s tests -v` to inspect structural fixtures and failure behavior. These are engineering examples, not evidence of a completed classroom manuscript.
