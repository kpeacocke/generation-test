---
name: review
description: Independently review the current change using the repository code-review methodology.
agent: reviewer
argument-hint: focus='optional review focus or risk area'
---

Review the current change independently. Follow the `code-review` skill. Focus additionally on: `${input:focus}`

Do not edit. Verify material findings where execution is available. Prefer a small number of proven findings over speculative commentary. Include coverage gaps and an advisory merge recommendation.
