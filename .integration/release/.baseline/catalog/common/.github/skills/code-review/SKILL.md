---
name: code-review
description: Rigorous, evidence-first code review for pull requests, diffs, patches, branches, commits, and local working trees. Use when asked to review code, a PR, changes, a patch, a branch, merge readiness, or to find defects before merge. Prioritizes correctness, security, reliability, compatibility, data integrity, tests, operability, and maintainability over style. Builds repository context and a risk map, runs three review passes, proves or dismisses suspected findings, executes repository-native tests and tools when available, separates introduced defects from pre-existing debt, distinguishes verified evidence from inference, assigns severity by impact and likelihood, and when edits are permitted iterates through regression test, smallest fix, targeted verification, broader checks, final diff inspection, and self-review. Requires an explicit blind-spot pass asking what the review is missing and what could still fail in production, records failed checks and coverage gaps, and finishes with an advisory merge recommendation plus exactly three high-leverage next actions the user did not ask for. For GitHub Copilot Code Review, the merge recommendation is advisory because Copilot posts comment reviews rather than approval/request-changes decisions; declare unsupported or excluded files as coverage gaps instead of implying they were reviewed.
metadata:
  version: "1.0.0"
  methodology: evidence-first risk-based three-pass review
---

# Evidence-first code review

## Mission

Find material defects and risk before they reach users. Do not optimise for comment count, stylistic preference, or appearing thorough.

A good review should answer:

1. What contract is this change meant to satisfy?
2. Where can it materially fail?
3. Which suspected failures can be proven or dismissed?
4. What remains unverified?
5. Is the change ready to merge?

## Non-negotiable principles

- Evidence over plausibility. Do not report a finding merely because a pattern looks suspicious.
- Impact over cosmetics. Correctness, security, reliability, compatibility, data integrity, and operability outrank style.
- Changed-code causality. Report pre-existing debt separately unless the change makes it newly reachable, materially worse, or necessary to understand a regression.
- Repository contract over reviewer taste. Prefer project conventions and documented requirements over personal preferences.
- Tests are evidence, not proof. Passing tests reduce uncertainty only for behaviour they actually exercise.
- Minimal scope. Do not turn a review into an unrelated redesign.
- Do not claim execution that did not occur. `Not run`, `blocked`, `inferred`, and `passed` are different states.
- Silence is preferable to a speculative low-value comment.

## Operating modes

Determine the mode from actual capabilities, not desired behaviour.

### Review-only mode

Use when the environment can inspect but must not modify the change, including GitHub Copilot Code Review and explicit read-only review requests.

- Inspect, search, and execute safe verification if available.
- Do not edit the reviewed branch or claim a fix was applied.
- Produce review findings and an advisory merge recommendation.
- On GitHub Copilot Code Review, remember that Copilot submits a `COMMENT` review. `APPROVE` and `REQUEST_CHANGES` in this skill are recommendations to the human/merge process, not GitHub review events.
- Explicitly disclose relevant files or artefacts the review surface cannot inspect. Do not imply full coverage when GitHub excludes a file type from Copilot review.

### Action mode

Use only when the environment permits edits and the user asked to fix, implement, action, or iterate rather than only review.

For each confirmed in-scope defect:

1. Reproduce or otherwise prove the defect where practical.
2. Add or identify a regression test/probe that fails for the causal reason.
3. Apply the smallest coherent fix.
4. Run targeted verification.
5. Run broader repository-native checks proportionate to risk.
6. Inspect the final diff for accidental changes.
7. Self-review the resulting change from scratch.
8. Repeat while material in-scope failures remain.

Do not refactor adjacent code merely because it can be improved. Fix collateral issues only when they block verification, create a material security/correctness risk, or are inseparable from the requested change. Call out the scope expansion.

## Phase 0 — Establish the review contract

Before judging implementation, determine:

- requested behaviour and acceptance criteria;
- base/head or before/after state;
- repository-local instructions and contribution rules;
- relevant ADRs, API/schema contracts, compatibility promises, generated-file rules, and security policy;
- CI/build/test expectations;
- whether the task is review-only or action mode.

Read the entire PR description, linked requirements available in the current context, and relevant surrounding code. Do not review a diff in isolation when neighbouring code defines its semantics.

If requirements are ambiguous, infer only what the repository and request strongly support. Label the ambiguity instead of inventing product requirements.

## Phase 1 — Build a change map and risk map

Summarise what actually changed by behaviour, not filename. Identify:

- externally observable behaviour;
- public API, schema, serialisation, protocol, CLI, or configuration changes;
- trust and privilege boundaries;
- persistent state, migrations, transactions, concurrency, retries, and idempotence;
- lifecycle and resource ownership;
- dependencies and supply-chain changes;
- build, deployment, CI, packaging, and infrastructure changes;
- generated artefacts or files that cannot be reviewed in the active surface.

Rank review attention using:

`risk = impact × likelihood × reachability × uncertainty`

Use this as prioritisation, not fake numeric precision.

Spend the most effort where state can be corrupted, privilege changes, untrusted input crosses a boundary, contracts change, failures are irreversible, concurrency is introduced, or tests give weak coverage.

For detailed domain prompts, load `references/review-checks.md` only for the affected domains. Do not mechanically run every checklist against every change.

## Phase 2 — Three review passes

### Pass 1 — Contract and architecture

Read the change at system level before line-by-line inspection.

Check whether:

- the implementation satisfies the stated outcome rather than a nearby problem;
- new complexity is necessary;
- existing abstractions or platform primitives should be used instead of parallel machinery;
- boundaries, ownership, lifecycle, and error propagation remain coherent;
- compatibility and rollout assumptions are explicit;
- the change introduces an implicit architectural decision that will be expensive to reverse.

Ask:

> What decision is this change accidentally making permanent?

### Pass 2 — Failure paths and adversarial behaviour

Trace important inputs and state through the changed code. Start with what can go wrong, not the happy path.

Check relevant cases including malformed/untrusted input, authentication/authorisation, permission transitions, partial failure, empty/boundary values, retries, duplicate delivery, timeouts, cancellation, race/restart/recovery, serialization and encoding, resource cleanup, data rollback, and dependency failure.

For security-sensitive changes, model source → validation → transformation → sink and principal → permission → protected operation. Load the security section of `references/review-checks.md`.

### Pass 3 — Verification and maintainability

Inspect tests and executable evidence. Ask:

- do tests assert externally meaningful behaviour rather than implementation trivia?
- would the tests fail if the suspected defect were present?
- are negative and failure paths covered where risk warrants them?
- were valid assertions weakened, deleted, skipped, or broadly ignored?
- do lint/static/type/build/security tools cover the changed path?
- will another engineer understand failure behaviour and operational consequences?

Maintainability findings are blockers only when they create a credible defect risk or materially increase the cost/risk of operating or modifying the changed path.

## Phase 3 — Prove or dismiss findings

Treat every suspected issue as a hypothesis.

For each candidate finding:

1. State the exact claim privately: `Under condition X, code Y causes outcome Z.`
2. Locate the causal path in changed code.
3. Check guards, callers, invariants, tests, and platform semantics that could invalidate the claim.
4. Search for existing coverage or documented intentional behaviour.
5. Reproduce with the smallest safe test/probe when execution is available and worthwhile.
6. Try to falsify the claim.
7. Report it only if evidence survives.

A pattern match alone is not proof. Examples: `shell=True`, disabled TLS verification, mutable default, broad exception, or missing null check can be dangerous, but report only when the changed code makes a material bad outcome reachable.

When reproduction is impossible, label the finding `strongly inferred` and state the missing evidence. Do not inflate uncertainty into certainty.

## Phase 4 — Execute verification

When safe execution is available, inspect repository-native entry points before inventing commands: CI workflows, `Makefile`, task runner, package scripts, build files, tox/nox, pre-commit, lint configuration, container/devcontainer setup, and contribution docs.

Establish a useful baseline before modifying code in action mode when practical.

Choose the smallest checks that meaningfully test the risk, then broaden:

1. reproducer/regression test;
2. affected unit/component tests;
3. relevant lint/type/static/security checks;
4. broader test suite;
5. build/package/integration checks where warranted.

Record commands, exit status, and material result. Preserve failed runs that informed the investigation.

If a tool is unavailable, dependency installation is blocked, credentials are unavailable, or the environment differs materially from production, state that as a coverage gap.

Never substitute code inspection for execution when execution is available and would materially reduce uncertainty.

## Phase 5 — Severity and comment threshold

Severity describes consequence plus credible reachability, not reviewer discomfort.

### Critical

Credibly reachable catastrophic impact such as remote code execution across a trust boundary, authentication bypass with broad privilege, irreversible widespread data loss/corruption, or secret compromise with major blast radius.

### High

Merge-blocking material failure: security control bypass, common-path crash/outage, data corruption/loss, broken public contract, unsafe migration/rollback, major privilege mistake, or deterministic incorrect behaviour with meaningful impact.

### Medium

Real defect with bounded impact, credible edge-case failure, resource/lifecycle leak, misleading operational behaviour, insufficient validation on a reachable path, or test gap that permits a significant regression.

### Low

Non-blocking issue with concrete future cost or limited behavioural impact. Do not use Low as a bucket for taste.

### Nit

Pure style/preferences. Omit by default unless the user explicitly requested style review or the repository enforces the rule automatically and the violation blocks CI.

Before posting a finding ask:

- Is it introduced or materially exposed by this change?
- Can I describe a concrete bad outcome?
- Can I identify the triggering condition?
- Did I check whether the code already prevents it?
- Is it worth the author's attention now?

If not, omit it or put it in clearly separated non-blocking debt.

## Finding format

Each reported finding must be independently actionable.

**[Severity] Short imperative title**

- **Location:** file and smallest useful line/range.
- **Condition:** exact state/input/path required.
- **Impact:** concrete bad outcome.
- **Evidence:** execution/reproducer, code path, contract, or authoritative semantics.
- **Fix direction:** smallest useful correction, without unnecessary redesign.
- **Confidence:** `verified` or `strongly inferred`.

Do not bury the trigger or impact in prose. Do not write essays when a compact causal explanation is enough.

## Phase 6 — Action loop

In action mode, findings are work items, not the finish line.

For a confirmed defect:

`prove → regression test → fail → smallest fix → targeted pass → broader checks → inspect diff → self-review`

If the proposed regression test passes before the fix, it did not prove that defect. Repair the test/probe or revise the hypothesis before changing production code.

If the smallest fix exposes a pre-existing blocker, stop and classify it rather than silently expanding scope.

After all fixes, re-read the final diff without relying on the earlier review conclusions. Look for accidental debug code, changed defaults, swallowed errors, weakened tests, generated noise, permission expansion, hidden compatibility changes, and new dependencies.

## Phase 7 — Mandatory blind-spot pass

Before concluding, answer and investigate:

> What is the most important thing the current review/request is missing?

Then:

> If this change fails in production despite the current tests passing, what is the most plausible reason?

Check at least the highest-risk answer against the code, tests, configuration, or platform semantics.

Also scan for negative space: expected files not changed, schema/client/docs not updated with an API change, migration without rollback, new configuration without deployment wiring, new behaviour without telemetry, and tests that never exercise the new branch.

## Decision

Choose one advisory recommendation:

- `APPROVE` — no known material blocker; evidence is proportionate to risk.
- `COMMENT` — no proven merge blocker, but material uncertainty or non-blocking issues remain.
- `REQUEST_CHANGES` — one or more proven/strongly supported merge-blocking defects remain.
- `BLOCKED` — review cannot reach a defensible conclusion because required context/evidence is unavailable.

On GitHub Copilot Code Review these are advisory labels in the review text. Copilot itself posts a Comment review and cannot satisfy required human approvals or request-changes gates.

## Final output contract

Always produce these sections, even when there are no findings:

### Decision

Advisory recommendation plus one-sentence rationale.

### Change and risk summary

What changed, highest-risk surfaces, and scope/coverage limitations.

### Findings

Ordered Critical → High → Medium → Low. If none, write `No material findings.`

### Verification evidence

- checks actually executed and result;
- reproductions/regression tests and whether they failed before the fix;
- failed checks/attempts encountered during the work;
- checks not run and why;
- relevant files excluded or unsupported by the review surface.

### Blind-spot pass

Answer both mandatory blind-spot questions and what was checked because of them.

### Residual risk

What remains uncertain after verification.

### Three high-leverage things you did not ask for

List **exactly three** next actions, ranked by expected value. For each explain why it matters now and offer to execute it. Prefer actions that reduce residual risk, prevent recurrence, improve observability, or simplify the system. Do not pad the list with generic process advice.

### Action-mode change log

Only in action mode: summarise defects proven, tests added, fixes applied, and the final verification state.

## What not to do

- Do not review generated/minified/vendor code line-by-line unless the task requires it.
- Do not flood a PR with formatting comments covered by automation.
- Do not ask for speculative defensive code without a reachable failure mode.
- Do not state `tests pass` when they were not run.
- Do not confuse a GitHub Copilot Comment review with repository approval.
- Do not hide review coverage gaps.
- Do not refactor the entire subsystem to fix a local defect.
- Do not lower tests, disable lint, broaden ignores, or catch-and-drop errors merely to achieve green.

## References

- Load `references/review-checks.md` for detailed domain-specific prompts when the change touches those domains.
- Use repository-local contribution and security documentation as higher-priority project context.
