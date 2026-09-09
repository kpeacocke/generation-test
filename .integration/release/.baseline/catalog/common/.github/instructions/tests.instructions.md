---
applyTo: "tests/**,**/test_*.py,**/*_test.py,**/*.spec.*,**/*.test.*"
description: Test design conventions for repository tests.
---

Tests should prove behaviour, not implementation trivia.

- Prefer deterministic tests with explicit setup and teardown.
- A regression test for a defect should fail for the causal reason before the fix.
- Cover meaningful negative/error paths at system boundaries.
- Do not weaken, skip, or delete valid assertions merely to make a change pass.
- Avoid excessive mocking that bypasses the behaviour under test.
- Make test names describe the contract being protected.
