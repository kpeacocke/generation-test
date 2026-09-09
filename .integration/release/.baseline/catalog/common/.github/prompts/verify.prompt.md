---
name: verify
description: Prove a behavioural claim by executing the relevant checks and reporting evidence.
agent: implementer
argument-hint: claim='behaviour or requirement that must be proven'
---

Prove this claim: `${input:claim}`

Use the `test-and-verify` skill. Establish observable acceptance criteria, execute the strongest available evidence, include a negative/failure-path check where useful, and distinguish verified facts from inferred or blocked checks. Do not modify unrelated behaviour while proving the claim.
