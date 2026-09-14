# ACT41 fresh-context recovery test

**Recorded:** 2026-08-29T18:37:39.2213777Z (the command completed before the
ACT41 state edits)  
**Input authority:** only the current files under `collatz_reconstruction`
(`state/project_state.json`, `state/coverage.json`,
`research_companion/MANIFEST.json`, the two declared PDFs, and the three
validators). No conversational summary or compaction text was read.

A new Python process independently:

1. parsed the durable state and checked the live goal thread
   `01a00ba5-a6b8-7410-b1e3-ab6dc0a4acf4` is active with
   `completion_claimed=false`;
2. checked that the current checkpoint is `ACT-COL-000041` and its audit file
   exists;
3. checked the 155-page working PDF and 18-page companion PDF hashes and the
   corresponding coverage values; and
4. reran `certificates/chatnotes_weighted_path_finite_actions.py`,
   `research_companion/certificates/finite_actions_checks.py`, and
   `research_companion/validate_package.py` as subprocesses, requiring JSON
   `status=PASS` from each.

The process emitted:

```json
{"checkpoint": "ACT-COL-000041", "commands": [{"command": "certificates/chatnotes_weighted_path_finite_actions.py", "status": "PASS"}, {"command": "research_companion/certificates/finite_actions_checks.py", "status": "PASS"}, {"command": "research_companion/validate_package.py", "status": "PASS"}], "companion_pages": 18, "completion_claimed": false, "goal_status": "active", "status": "PASS", "working_pages": 155}
```

This is a successful recovery of the sealed artifact checkpoint, not a claim
that the wider literature-first Collatz corpus is complete.  The recovery
record itself is external state and is not part of the portable package.
