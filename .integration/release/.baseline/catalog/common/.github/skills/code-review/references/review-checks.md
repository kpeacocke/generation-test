# Domain review checks

Load only the sections relevant to the changed risk surface. These are prompts for investigation, not a requirement to manufacture findings.

## Security and trust boundaries

Trace untrusted input from source through validation/transformation to sensitive sink.

Check as applicable:

- authentication versus authorisation and object-level access;
- injection into shell, SQL, template, path, expression, URL, LDAP, YAML, or deserialiser sinks;
- traversal, archive extraction, symlink and filesystem-boundary issues;
- SSRF and network egress controls;
- secret/token/password handling, logs, exception text, temporary files, and build artefacts;
- cryptographic purpose, approved primitive/mode, randomness, key storage, rotation, expiry, and certificate verification;
- TLS verification and hostname validation;
- CSRF/CORS/cookie/session controls for web paths;
- dangerous deserialisation and parser limits;
- privilege changes, confused-deputy paths, tenant isolation, and default permissions;
- denial-of-service via unbounded input, allocation, regex, recursion, fan-out, retries, or decompression;
- TOCTOU and validation/use gaps.

Try one negative or bypass case for the most important security boundary when executable.

## API, protocol, schema and compatibility

Check:

- backwards/forwards compatibility and version negotiation;
- required versus optional fields and changed defaults;
- unknown enum/value handling;
- serialization precision, ordering, encoding, nullability, timezones and units;
- pagination, retries, idempotency keys, duplicate delivery, and partial responses;
- consumer/client/schema/docs updates;
- deprecation and rollout plan;
- old and new component version interoperability.

Ask what happens during mixed-version deployment.

## Data, persistence and migrations

Check:

- migration safety on existing data, not only empty databases;
- transactional boundaries and partial commits;
- uniqueness/foreign-key/invariant preservation;
- backfill performance and locks;
- retry/idempotence;
- rollback/roll-forward and downgrade compatibility;
- destructive schema changes and data retention;
- concurrent old/new writers.

Test representative old-state data when practical.

## Concurrency, async and distributed behaviour

Check:

- race conditions and atomicity;
- lock scope/order and deadlocks;
- cancellation and timeout propagation;
- lost updates and duplicate work;
- retry storms/backoff/jitter;
- at-least-once versus exactly-once assumptions;
- ordering and eventual consistency;
- restart/recovery state;
- connection/task/thread/goroutine lifecycle.

Ask what happens immediately before, during, and after process restart.

## Resource and lifecycle management

Check files, sockets, streams, processes, temporary directories, locks, transactions, subscriptions, handles, memory, GPU/device resources, and cloud resources for:

- ownership;
- cleanup on success and exception/cancellation paths;
- repeated-call behaviour;
- upper bounds and exhaustion;
- shutdown ordering.

## Dependencies and supply chain

Check:

- why a new dependency is required and whether existing platform/library capability already solves it;
- direct/transitive footprint;
- version pinning and lockfile consistency;
- maintainer/release health;
- known vulnerabilities/advisories;
- licence/policy compatibility;
- package-name confusion/typosquatting;
- install/build scripts and network access;
- third-party GitHub Action pinning to immutable commit SHA;
- provenance/signatures where the ecosystem supports them.

Treat dependency files excluded from a review surface as a declared coverage gap, not as reviewed.

## CI/CD, infrastructure and GitHub Actions

Check:

- workflow token permissions and untrusted PR contexts;
- `pull_request_target`, reusable workflows, environment protections and secrets;
- expression-to-shell injection;
- action pinning and supply-chain trust;
- cache poisoning and artefact trust boundaries;
- deployment concurrency and rollback;
- Terraform/provider state and destructive changes;
- network exposure/security groups/firewall paths;
- immutable versus mutable deployment inputs.

## CLI and automation

Check:

- exit codes;
- stdout/stderr contracts;
- signal/cancellation behaviour;
- non-interactive operation;
- paths with spaces/unicode/metacharacters;
- idempotence;
- partial failure and resumability;
- secret-safe logging;
- dry-run/check-mode semantics.

## Tests

Check whether tests:

- prove externally meaningful behaviour;
- fail before the fix for the correct reason;
- cover both happy and important failure paths;
- avoid over-mocking away the real boundary;
- remain deterministic;
- validate old-state/backwards compatibility where needed;
- were weakened, skipped, or deleted by the change;
- leave critical changed branches unexercised.
