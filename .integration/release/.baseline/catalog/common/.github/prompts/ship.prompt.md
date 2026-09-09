---
name: ship
description: Finish the smallest useful version instead of expanding scope.
agent: implementer
argument-hint: outcome='what must be usable when this is done'
---

Ship the smallest useful version of: `${input:outcome}`

Before editing, identify the minimum acceptance criteria and explicitly list adjacent improvements that are **not** required now. Implement only the bounded outcome, prove it with `test-and-verify`, run `pr-preflight`, and stop when the useful version is complete unless a discovered issue is a correctness, security, or operability blocker.
