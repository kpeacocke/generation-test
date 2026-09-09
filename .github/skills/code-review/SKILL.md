---
name: code-review
description: Evidence-first, risk-based review of pull requests, diffs, commits, patches, and changed code. Use for GitHub Copilot code review or when asked to review, audit, inspect, approve, critique, or validate a code change. Find material correctness, security, reliability, compatibility, test, operability, maintainability, and scope risks; prove findings with repository context and executable evidence; distinguish review-only from action mode; and drive confirmed issues through fix, regression test, and re-verification when write and execute access exists.
metadata:
  version: "1.1.0"
---

# Code Review

Find the smallest set of material issues that could make the change unsafe, incorrect, brittle, incompatible, or expensive to operate. Prove each finding. Do not optimise for comment count.

## Non-negotiable rules

- **Evidence beats intuition.** A defect needs a violated contract plus a concrete trigger/failure path, repository evidence, tool output, or reproduction.
- **Review in context.** Read relevant callers, tests, schemas, configuration, CI, docs, and repository instructions; do not judge only the diff.
- **Prioritise material risk.** Correctness, security, data loss, compatibility, reliability, and operability outrank style.
- **Do not rubber-stamp.** Passing tests are evidence, not proof; inspect what they do not cover.
- **Do not report speculative bugs as findings.** Investigate first; unresolved suspicion belongs under open/unverified risk.
- **Do not fake execution.** Never say a command, test, scan, build, or reproduction ran unless you observed it run.
- **Do not widen scope silently.** Separate unrelated pre-existing debt from regressions introduced by the change.
- In action mode, do not stop at commentary: prove, regression test where practical, make the smallest safe fix, and re-verify.

## Determine the operating mode

### Review-only mode

Use for GitHub Copilot Code Review, review-only requests, or read-only environments.

- Do not modify code.
- Report only actionable, evidenced findings.
- Give the smallest safe fix direction.
- `APPROVE` / `REQUEST CHANGES` is advisory when the host cannot set that review state.
- State coverage gaps when material files or checks could not be reviewed.

### Action mode

For each confirmed in-scope defect: prove it -> add/identify a regression test -> smallest safe fix -> targeted check -> broader relevant checks -> inspect diff -> self-review -> repeat until green or blocked by a concrete environmental constraint.

Never weaken a valid test merely to make a build pass.

## Phase 0 — Establish the review contract

Discover what correct means before judging code. Read the PR intent/acceptance criteria and relevant repository instructions, tests, public interfaces, manifests/lockfiles, CI/build configuration, callers, schemas, migrations, and rollout notes. If intent and implementation disagree, report it rather than guessing.

## Phase 1 — Build a change and risk map

Identify changed behaviour, touched subsystems, public contracts, trust boundaries, state transitions, dependencies, compatibility/migration/rollback implications, and claimed versus actual test coverage. Classify overall risk as high/medium/low and spend review effort accordingly.

For large changes, explicitly state coverage limits instead of pretending every line received equal scrutiny.

## Phase 2 — Review in three passes

### Pass A — Intent, design, and contracts

Check requirement fit, backwards compatibility, defaults, migrations, rollback, hidden coupling, unnecessary abstractions, duplicated capability, and unrelated scope creep. Ask whether a substantially simpler design exists.

### Pass B — Correctness, security, and failure behaviour

Trace reachable data/control paths. Check relevant boundary values, malformed/adversarial input, state ownership, retries/idempotency, concurrency, partial failure, timeouts/cancellation, authn/authz/object scoping, injection/path traversal/SSRF/deserialisation, secret exposure, transactions/rollback, cache invalidation, resource growth, and restart/scale-out behaviour.

### Pass C — Tests, maintainability, and operations

Check that tests encode behaviour and can fail; changed behaviour and failure paths are covered; assertions were not weakened; dependencies/supply chain are justified; errors/logs remain useful and safe; complexity is proportional; compatibility/rollout is managed; and operational signals/recovery remain meaningful.

Load `references/review-checks.md` for the detailed domain matrix when needed.

## Phase 3 — Prove or dismiss suspected findings

Evidence strength, strongest first:

1. failing regression test or deterministic reproduction;
2. compiler/type/static/security tool output tied to the reachable changed path;
3. existing test or documented contract directly contradicted by the change;
4. traceable input/state -> faulty operation -> observable impact;
5. authoritative external documentation when behaviour depends on it.

For a suspected defect: state the invariant, trigger, changed path, faulty outcome, impact, then run a focused probe when execution is available. Dismiss concerns that do not survive investigation. Record material failed probes/disproven hypotheses as verification evidence, not findings.

## Phase 4 — Execute repository-native verification

Discover and prefer the repository's own commands/CI. Run the smallest relevant checks first, then broaden: targeted tests -> affected suite -> formatter/linter/type checker -> build/package -> integration/e2e -> security/dependency checks -> broader suite when proportionate.

For every executed check retain command, exit status, meaningful result, failing names, and whether a failure is introduced, pre-existing, environmental, or unresolved. A check not run is never a pass.

## Phase 5 — Severity and merge decision

**Severity is impact, not confidence.** Track confidence separately.

- **BLOCKER**: credible security compromise, data loss/corruption, catastrophic outage, or fundamental contract failure.
- **HIGH**: material correctness/reliability/security/compatibility/production-operability failure.
- **MEDIUM**: real bounded defect or material maintainability/performance problem.
- **LOW**: worthwhile low-risk improvement.
- **NIT**: cosmetic preference; omit when automated tooling handles it.

Confidence: **High** = reproduced/tool-proven/unambiguous; **Medium** = strong code-path evidence; **Low** = unresolved suspicion, which must not be listed as a defect.

Decision:
- **REQUEST CHANGES** for unresolved BLOCKER/HIGH or a MEDIUM that clearly makes the change unsafe/incorrect.
- **APPROVE WITH FOLLOW-UPS** when no material blocker remains but useful non-blocking work exists.
- **APPROVE** when no material issue is found and verification is adequate for the risk.
- **INCOMPLETE** when missing context/tooling prevents a responsible conclusion.

## Phase 6 — Action loop in action mode

For each confirmed issue: capture before-state proof -> smallest coherent fix -> encode corrected behaviour in tests -> targeted verification -> broader checks -> inspect diff for accidental scope/debug/secrets/weakened assertions -> self-review Passes A-C -> repeat. Do not claim completion while known in-scope failures remain.

## Mandatory blind-spot pass

Before finalising, investigate:

> What is the most important thing the current review/request is missing?

Look for one high-leverage blind spot outside the obvious lines: caller, unstated invariant, migration/rollback path, privilege boundary, failure mode, operational dependency, test oracle, compatibility constraint, or simpler design. If none survives investigation, say so.

Then investigate:

> If this change fails in production despite the current tests passing, what is the most plausible reason?

## Output contract

Keep inline comments sparse. Each defect finding must include severity, confidence, precise location/symbol, violated invariant, concrete trigger/failure path, impact, evidence, smallest safe fix direction, and verification needed after the fix.

Final review summary, in order:

1. **Decision** — APPROVE / APPROVE WITH FOLLOW-UPS / REQUEST CHANGES / INCOMPLETE.
2. **Risk summary**.
3. **Findings** ordered by severity, or `No material findings`.
4. **Verification evidence** — commands/checks actually run, results, material failures encountered, and important checks not run.
5. **Most important thing you may be missing** — investigated blind spot or `No material blind spot found`.
6. **Three high-leverage things you did not ask for** — exactly three concrete follow-ups, ranked 1-3, each with one-sentence rationale and an offer to execute it.

In action mode also include **Changes made** and **Residual risk**.

## Anti-patterns to reject

Do not summarise the diff and call it review; praise routine code instead of testing failure modes; infer safety from coverage alone; trust new tests without checking their assertions; accept swallowed exceptions/silent fallback/disabled validation without understanding the contract; demand rewrites when a local fix works; confuse pre-existing debt with regression; cite irrelevant tool warnings; or use vague comments such as “consider security”, “might race”, or “add more tests” without a concrete scenario.
