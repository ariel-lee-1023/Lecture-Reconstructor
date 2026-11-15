# Recovery impact check

Recorded UTC: 2026-11-15T02:16:39.552799+00:00. Actually ran the current package's check_run before recovery; exit code 0.

The original and normalized input snapshots and six files in the old runtime record were compared individually and are unchanged. Original chapter 1 does not require invalidation for a version change. Continue from run.resume, while still checking the old chapter against the whole source again.

Additionally read transcript-repair.md in this run. No ASR repair was needed and the transcript was not modified. Its loading and hash will be truthfully added to runtime; this is not a core-version change. Earlier semantic evidence retains its original hashes.

Other-branch paths in the original audit/checkpoint appeared only as old record content and were not accessed in this run. No network, upstream repository, package/evals, or other branch was read.
