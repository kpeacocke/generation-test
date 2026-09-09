---
applyTo: ".github/workflows/**/*.yml,.github/workflows/**/*.yaml"
description: Security and maintainability rules for GitHub Actions workflows.
---

Treat workflow code as privileged production code.

- Declare minimum `permissions` explicitly at workflow or job level.
- Pin third-party actions to a full commit SHA. A floating tag such as `@v4` is not sufficient for the managed baseline.
- Avoid interpolating untrusted event data directly into shell scripts. Pass values through environment variables and quote them.
- Do not print secrets or credentials.
- Prefer `pull_request` over `pull_request_target`; use privileged triggers only with an explicit threat model.
- Avoid broad write tokens where a narrower permission works.
- Add timeouts to long-running jobs where hanging is credible.
- Make failure visible; do not hide required checks behind `continue-on-error`.
