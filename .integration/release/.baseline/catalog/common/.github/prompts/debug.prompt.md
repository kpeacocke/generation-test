---
name: debug
description: Reproduce and root-cause a concrete failure before fixing it.
agent: implementer
argument-hint: problem='error, failure or symptom'
---

Debug this problem: `${input:problem}`

Follow the `debug-root-cause` skill strictly. Preserve evidence, reproduce before editing when practical, test competing hypotheses, and do not stop at a plausible explanation. If a fix is in scope, establish regression evidence, apply the smallest fix, and prove the original symptom is gone. Include failed attempts in the evidence trail.
