---
name: refactor-arch
description: >
  Audits and refactors legacy codebases to MVC architecture.
  Use when the user asks to "/refactor-arch", audit architecture,
  detect anti-patterns, or refactor to MVC/SOLID.
---

# refactor-arch

Automated architecture audit and MVC refactoring skill. Technology-agnostic: works with Python/Flask and Node.js/Express.

## When to Activate

User invokes `/refactor-arch` or asks to audit/refactor a legacy project to MVC.

## Reference Files

Read before each phase:
- `references/project-analysis.md` — Phase 1 heuristics
- `references/anti-patterns-catalog.md` — Phase 2 detection rules
- `references/audit-report-template.md` — Phase 2 output format
- `references/mvc-guidelines.md` — Phase 3 target architecture
- `references/refactoring-playbook.md` — Phase 3 transformations

Optional scripts:
- `scripts/detect_stack.py` — stack detection helper
- `scripts/validate_endpoints.py` — post-refactor smoke test

## Workflow

Execute phases **sequentially**. Never skip Phase 2 confirmation.

### Phase 1 — Analysis

1. Scan project root for manifest files and source extensions
2. Apply heuristics from `project-analysis.md`
3. Print `PHASE 1: PROJECT ANALYSIS` block (exact format in reference)
4. Do NOT modify any files

### Phase 2 — Audit

1. Read all source files in project (exclude node_modules, __pycache__, .git)
2. Cross-reference against every anti-pattern in `anti-patterns-catalog.md`
3. Record exact file:line for each finding
4. Classify severity: CRITICAL, HIGH, MEDIUM, LOW
5. Check for deprecated APIs (AP10)
6. Generate report using `audit-report-template.md`
7. Order findings CRITICAL → LOW
8. Print: `Phase 2 complete. Proceed with refactoring (Phase 3)? [y/n]`
9. **STOP and wait for user confirmation. Do not modify files.**

### Phase 3 — Refactoring (only after user confirms)

1. Follow `mvc-guidelines.md` for target structure
2. Apply transformations from `refactoring-playbook.md` in order:
   - Security first (secrets, SQL injection, remove dangerous endpoints)
   - Config module
   - Models with parameterized queries
   - Services for business logic
   - Thin controllers
   - Views/routes registration only
   - Centralized error handler
3. Preserve original URL paths and response shapes where possible
4. For partially organized projects: improve layers, wire dead services, fix security
5. Validate:
   - Install dependencies
   - Boot application
   - Hit original endpoints (health, main CRUD)
6. Print `PHASE 3: REFACTORING COMPLETE` with new structure and validation checklist

## Severity Definitions

- **CRITICAL:** Architecture/security failures, SQL injection, hardcoded secrets, God Class
- **HIGH:** Strong MVC/SOLID violations, missing auth, fat controllers, global state
- **MEDIUM:** N+1, duplication, deprecated APIs, unsafe config
- **LOW:** Magic numbers, poor naming, print-based logging

## Technology Mapping

| Concern | Python/Flask | Node/Express |
|---------|-------------|--------------|
| Config | `config/settings.py` | `config/settings.js` |
| Routes | `views/routes.py` | `routes/*.js` |
| Controllers | `controllers/*.py` | `controllers/*.js` |
| Models | `models/*.py` | `models/*.js` |
| Errors | `middlewares/error_handler.py` | `middlewares/errorHandler.js` |
| Entry | `app.py` | `src/app.js` |

## Important Rules

- Minimum 5 findings in Phase 2
- At least 1 CRITICAL or HIGH per project
- Never log credit card numbers or secrets
- Remove `/admin/query` style endpoints if found
- Do not break existing API contracts during refactor
