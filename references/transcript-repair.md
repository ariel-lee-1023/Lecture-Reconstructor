# Optional Transcript Repair

Load this reference only when transcription damage affects understanding. Its methods are adapted from `transcript-proofreader/SKILL.md`. Proofreading preserves the original transcript language; the subsequent manuscript uses the language explicitly requested by the user, or the course language when none is specified. This stage restores a readable classroom record, after which course reconstruction is still required. It does not restrict authorized reordering, added explanation, or reconstruction of the teaching voice.

## Preserve evidence before repairing

Keep the original file unchanged and read-only. Save normalized text and any necessary cleaned version separately, maintaining correspondence between original and derived texts. Read TXT and Markdown directly; preserve SRT/VTT timestamp lines, speaker labels, and valid text as location information. If timestamps are damaged, describe the readable scope and unavailable time locations, then continue using original text line locations. Do not infer new timestamps or claim to have listened to audio that was not supplied.

Read surrounding context first, distinguishing ASR damage, acceptable spoken language, the speaker's memory or factual errors, and substantive positions. Removing meaningless stumbles and empty fillers can improve readability; do not mechanically delete negations, self-corrections, logical connections, emphasis, or the actual referent of “this.” Repeated substantive propositions may be merged during reconstruction with their destinations recorded; proofreading must not silently delete small examples or objections first.

## Repair, preserve, or ask according to the evidence

| Situation | Action |
|---|---|
| Context, syntax, repeated terminology, and confirmed entities jointly support a recoverable meaning | Make the smallest repair. When meaning is clear but the original wording is not unique, record it as “inferred from context”; routine repairs need not all be returned to the user. |
| The wording is unusual but meaningful, or the position is disputed | Preserve its attribution; disagreement is not evidence of an ASR error. |
| Two readings change the actor, event, number, negation, causation, or core term | Preserve the unresolved passage and candidates, ask the smallest question that resolves the ambiguity, and record blocking status and its reason. |
| External material can confirm only a name's spelling | Use it only to establish spelling or background; it does not prove that the speaker said that name. |

When there are real candidates, compare the original wording and candidates for phonetic similarity, local syntax, topic, and usage elsewhere in the course; also consider that the original reading may be correct. Do not invent candidates to fill a quota or add events merely because a story is familiar. Numbers, percentages versus percentage points, units, and ranges require separate checking. Correct arithmetic does not establish which number the speaker intended.

**English adaptation of this project's synthetic example:** The transcript says “This clam corresponds to the other party's duty,” while surrounding passages repeatedly use “claim.” Repair “clam” to “claim” on the basis of the course's terminology and the sentence's meaning. In another sentence, “This transfer is valid / invalid,” both readings remain in the transcript and later material provides no basis for distinguishing them. Do not choose the one that seems more plausible. This changes the core legal consequence: first write the concept explanations that can be established, and leave the example's conclusion pending confirmation. The whole manuscript's status is `needs_input` or `partial`, not complete. Neither situation permits a claim of “confirmed by listening to the audio.”

## Carry decisions consistently across chapters

The run record's `terms` stores observed variants, the chosen form, confirmed or unresolved status, grounds, and affected locations. An unconfirmed identity does not become confirmed merely through repetition. When new evidence changes a term, revisit chapters already written. For consequential repairs, preserve the original text, correction, reason, and location of the supporting evidence; ordinary punctuation does not require an itemized ledger.

After repair, hand the normalized text, significant changes, and unresolved issues to the [Reconstruction workflow](reconstruction-workflow.md). Subsequent work may reorganize arguments, add explanations, and merge repetition, but must not impersonate the original wording or erase unresolved core meaning. `notes.md` records only important corrections and unresolved issues; the main deliverable is `lecture.md`. Do not inherit the proofreading skill's English default, person-specific glossaries, editorial notes as the main deliverable, or linked Word/PDF requirements.

## Sources and boundaries

The actual adaptation source is the upstream `transcript-proofreader/SKILL.md`, revised November 11, 2026, specifically **Default: a clean oral record**, **Repair obvious ASR damage proactively**, **Make the evidence change the decision**, and **Carry decisions through the whole job**. Proactive contextual repair, entity memory, and decisions carried across passages are editorial designs of that upstream project; do not describe them as measured ASR performance.

The upstream skill states that its editing principles draw on Einsohn and Schwartz's *The Copyeditor's Handbook* (2019), Carol Fisher Saller's *The Subversive Copy Editor* (2009), and Hill and King's *Guide to the Transcripts of the Black Women Oral History Project* (1991). This project did not read those book modules and **does not inherit book-level details or add new chapter locations on that basis**. Attribution for this file's methods stops at the SKILL sections actually read; see the [Source manifest](../fidelity-ledger/source-manifest.json) for full version identities. These methods support careful repair; they do not establish transcription accuracy or replace substantive verification of course facts.
