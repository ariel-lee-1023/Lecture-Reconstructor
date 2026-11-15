# Chapter 3 direct review against the source

UTC: 2026-11-15T02:25:59.925616+00:00. Self-review by the executing agent (Codex desktop, exact model unknown), not independent review. Actual chapter SHA: 56935b264e4595052afa3b1ed49f741ac3131b60986bc4f5c64130f6e9b1641a. Reread the saved chapter, compared source lines 14–21, and checked the preceding two chapters' premises.

| Source line | Anchor | Actual checks |
|---|---|---|
| 14 | ch3-calculation | 10 per hour/5 per half-hour; whole half-hours only; overlap of valid reservation and closure, excluding time before the reservation. pass |
| 15 | ch3-ren | I reserves 10:00–12:00; closure 9:30–10:30; overlap 10:00–10:30 yields a refund of 5. Refunding 10 wrongly includes a half-hour outside the reservation; 10:30–12:00 remains valid. pass |
| 16 | ch3-review | Counting starts the day after knowledge; application receipt determines timeliness. Checks facts and rules, presumes no administrator correctness, and adds no automatic suspension. pass |
| 17 | ch3-gui | Thursday knowledge → Friday day 1 through the next Thursday day 7, shown day by day. Receipt before that day's end is timely; without a knowledge date, timeliness cannot be judged. pass |
| 18 | ch3-geng | Main facts remain sending at 17:58 and receipt at 18:02. One hour of closure requires refund 10; 5 already refunded leaves another 5, net debit 10. Submission and receipt the next Wednesday fall on day 6; procedure and substance remain separate. pass |
| 19 | ch3-variant | Only receipt at 17:59 changes the cancellation condition. Extinction of the reservation removes L3's valid-reservation prerequisite; no automatic refund of 10 or 0, and L2's settlement gap is retained. pass |
| 20 | ch3-exam | Retains teacher attribution, four steps for complete cases, the conceptual-comparison exception, and no promise about actual marking. pass |
| 21 | ch3-synthesis | Returns to G and four distinctions; inferences are confined to synthetic rules, without prior-lecture assumptions. pass |

Added calculations (H's refund of 10, G's additional refund of 5/net debit of 10) follow directly from the supplied L3/L4 and intervals, not new external rules. Full paragraphs explain how conditions enter the reasoning. No critical defects; pass; revision rounds 0. Real classroom trial and learning outcomes: not_run.
