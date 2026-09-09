---
name: plan
description: Investigate a change and produce a smallest-useful architecture and implementation plan before editing.
agent: architect
argument-hint: goal='outcome, problem or feature to plan'
---

Plan this goal: `${input:goal}`

Acquire repository knowledge before proposing a solution. Identify current architecture, constraints, trust and failure boundaries, compatibility concerns, likely files/components, and testable acceptance criteria.

Challenge scope. Explicitly answer:

1. What is the most important thing we are missing?
2. What decision would become expensive to reverse?
3. What can be deferred from the smallest useful version?

Return a sequenced implementation plan suitable for handoff to the implementer agent.
