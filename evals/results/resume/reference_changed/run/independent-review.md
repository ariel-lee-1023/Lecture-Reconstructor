# A08 reference_changed independent review

Conclusion: **pass**. No blocking defect found. After directly reading all 21 original lines and the current complete 186-line manuscript, checked rules, counterexamples, timed events, and whole-course connections. Content mappings and the generator's self-reported pass did not replace manuscript review.

Main manuscript: `resume-reference_changed/run/lecture.md`<br/>
SHA-256: `0c90bb769e3e96f28a8066e6222a2ca84b179a859a4e7cf3e419e9f3a35d53eb`<br/>
Review UTC: `2026-11-15T02:33:10.916977+00:00`

## Recovery evidence

1. **Input unchanged.** The original checkpoint, historical branch copies, and current raw/normalized inputs all have `077c32eeca35ff419d727aeb8fe93e4aff404deb67943a64a28978098741a0d6`. The original checkpoint run, Chapter 1, its old review, and historical copies match byte for byte; old evidence was not overwritten.
2. **The reference genuinely changed.** The recorded original hash is `d4330c05bc80cb47834ba627f2a4290d004a2b2ad48bd85bc352586a91af66e3`; the current hash is `07a2fa38245585dc499dbd47b1ad7c34015a199a3790421fff32a3d9e1b08f07`. Independently removing the exact added suffix, “Review for this resumption: for cases involving time conditions, check each event name, time, and rule trigger; do not merely check whether the numbers match,” reproduces the old hash. All other recorded runtime files are unchanged.
3. **Detection and invalidation preceded refreshing.** `pre-resume-check.json` and `checks/resume-initial.json` record RUNTIME_CHANGED/exit 2. This reviewer actually ran the current checker on `before-resume-run.json` and `invalidated-run.json`; both returned 2. The invalidated snapshot still retains the old reference hash, needs_review for all three chapters, and not_run for the active whole-manuscript semantic review. The old pass/date/chapter hashes were moved into historical_checks, and hash_refresh_status is not_yet_refreshed.
4. **The impact analysis is specific.** `impact-analysis.md` accurately identifies the new requirement. Its checks cover confirmation, sending/receipt, closure/reopening/expiry, overlapping intervals, learning of the decision/receipt of the application, and the 17:59 variant. It does not treat a method change as a change to rules or facts.
5. **There is new review evidence.** `checks/chapter-1-resumed-semantic.md` rechecks Monday confirmation, Wednesday performance, and the L1 trigger. Chapter 1 retains its original body hash, but the new review is recorded independently rather than rebinding an old pass. Chapters 2 and 3 have drafted-to-reviewed snapshots and source-by-source evidence; whole-manuscript evidence is bound to the current manuscript hash. The final run records all three chapters as assembled and status complete; this reviewer independently ran the final checker, which returned 0.

This evidence supports actual impact analysis and fresh review, rather than merely refreshing hashes and continuing blindly. The historical sequence remains a conclusion supported by preserved snapshots and dates, not proof from an external tamper-proof execution log.

## Direct verification against the source

| Original line | Manuscript line | Verification result |
|---|---|---|
| 1 | 7, 7 | Retains the synthetic identity, exclusion of current law/real classroom claims, and absence of preceding or subsequent lecture materials. |
| 2 | 10, 12, 153, 161 | The whole task of Monday confirmation for Wednesday 10:00–12:00 is resolved in chapter 3. |
| 3 | 17, 19, 29, 33 | L1 distinguishes permission from the administrator's duty to provide a standard seat; clicking, queuing, and receipt do not equal successful confirmation. |
| 4 | 38, 47 | A has no basis to demand that B give up a seat; D has a corresponding claim against the administrator. Both relationships coexist, and the duty is not transferred to B. |
| 5 | 52, 54 | Retains the peripheral charging-cable example: no priority or delivery promise, and no transplantation of the seat rule. |
| 6 | 22, 24 | Fully retains the objection that permission is useless and the response distinguishing what each relationship concerns. |
| 7 | 59, 63 | Chapter 1 establishes only formation of the relationship, without prejudging guaranteed performance through 12:00. |
| 8 | 73, 77 | L2 requires receipt no later than 18:00 on the preceding day, including exactly 18:00. Sending differs from receipt, and negotiation requires both parties' agreement. |
| 9 | 82, 87 | E's notice sent at 17:50/received at 18:05 fails; F's received at 18:00 succeeds. Cancellation does not terminate membership or permission. |
| 10 | 92, 94 | Retains L3's immediate safety hazard, power to suspend/duty to refund, absence of automatic cancellation, continuing validity of the remaining interval, and no extension. |
| 11 | 97, 99, 127, 127 | H reserves 10:00–12:00; closure lasts 10:00–11:00 and reopening occurs at 11:00. Arrival at 11:30 still leaves expiry at 12:00; the refund of 10 is calculated only after L4 supplies the rate. |
| 12 | 102, 102 | Retains the objection demanding a full refund whenever the entire reserved time is unused; personal lateness is distinguished from closure effects. |
| 13 | 107, 113, 155, 155 | G sends on Tuesday at 17:58; receipt is at 18:02, with no evidence of agreement. Wednesday suspension is 10:00–11:00, reopening 11:00, expiry 12:00. |
| 14 | 123, 127 | L4 charges 10 per hour/5 per half-hour, using whole half-hours only. L3 counts only the overlap of valid reservation and closure. |
| 15 | 132, 136 | I's closure at 9:30–10:30 overlaps the 10:00–12:00 reservation by half an hour, yielding a refund of 5. Explains why refunding 10 is wrong and why the remainder stays valid. |
| 16 | 141, 143 | L5 counts from the day after learning of the decision, requiring receipt before the end of day 7. It checks rules/time facts, presumes no administrator correctness, and adds no automatic suspension. |
| 17 | 146, 148 | J learns on Thursday, making the following Thursday day 7. A missing knowledge date cannot be replaced with an invented deadline conclusion; the calculation is limited to the exercise. |
| 18 | 153, 161 | G's debit of 20 follows the rate; refund due 10, already refunded 5, additional refund 5, correct net debit 10. An application sent and received the next Wednesday falls on day 6; procedural timeliness is separate from substantive grounds. |
| 19 | 166, 170 | Receipt at 17:59 is explicitly a variant. Timely cancellation removes L3's prerequisite; L2's settlement gap remains, with no invented refund of 0/10/all points. |
| 20 | 175, 177 | Retains attribution of the teacher's advice, the four steps for complete cases, the exception for conceptual comparisons, and no guarantee about real examination marking. |
| 21 | 182, 186 | Returns to four distinctions, stays within the synthetic rules, invents no prior-lecture premises, and claims no actual learning outcomes. |

Connections across the three chapters appear at manuscript lines 10–12, 61–68, 113–118, 153–161, and 182–186: formation establishes the relationship for later analysis; cancellation/suspension determines valid intervals; chapter 3 then calculates and separately reviews the application deadline. G's opening whole task and H's foreshadowed rate calculation are completed without assuming an earlier lecture proved anything. G's main facts consistently remain sending at 17:58 and receipt at 18:02; 17:59 is expressly confined to a variant.

Defects: no blocking or nonblocking content defects identified. This is a bounded direct source review and cannot exhaust problems that future materials might trigger.

## Independence and scope of the conclusion

- This review agent did not participate in generating the branch. It first directly read the original 21 lines and complete 186-line manuscript, then the generating agent's self-review evidence. Generation and this review belong to the same model system; they are neither independent human review nor cross-model replication.
- Read only the designated original checkpoint run, the reference_changed run/pre-resume-check, and necessary package SKILL/references/checker. The initial inventory listed other package paths without opening their contents. No other recovery branches were read and no online research was performed.
- The historical sequence is based on preserved snapshots, recorded dates, different states, and reproducible hash checks. This reviewer did not witness the original recovery as it happened; the records are not an external tamper-proof log.
- Conclusions are limited to this 21-line synthetic recovery fixture and the current manuscript. They establish neither context limits, real classroom trials, nor learning outcomes. Mechanical exit 0 establishes only bounded structural constraints.

Real classroom trial: not_run. Learning outcomes: not_run. Context-limit test: not_run.
