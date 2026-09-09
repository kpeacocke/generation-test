---
name: preflight
description: Decide whether the current change is actually ready for a pull request.
agent: implementer
---

Run the `pr-preflight` skill against the current working tree. Compare the final diff to the requested outcome, execute relevant repository-native checks, identify accidental scope and delivery gaps, and return READY, READY WITH WARNINGS, or NOT READY with evidence.
