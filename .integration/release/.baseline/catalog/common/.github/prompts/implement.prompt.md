---
name: implement
description: Implement a bounded outcome and prove it with repository-native checks.
agent: implementer
argument-hint: outcome='desired behaviour or acceptance criteria'
---

Implement this bounded outcome: `${input:outcome}`

Understand the affected contract first. Keep the change as small as possible, add or update regression protection, follow `test-and-verify`, inspect the final diff, and finish with `pr-preflight`. Do not expand the feature merely because adjacent improvements are visible.
