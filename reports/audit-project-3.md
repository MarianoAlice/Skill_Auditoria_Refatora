================================
ARCHITECTURE AUDIT REPORT
================================
Project: task-manager-api
Stack:   Python + Flask
Files:   15 analyzed | ~1200 lines of code

## Summary
CRITICAL: 5 | HIGH: 3 | MEDIUM: 5 | LOW: 1

## Findings

### [CRITICAL] No Authentication on API Endpoints
File: routes/user_routes.py:10-211; routes/task_routes.py:11-299
Description: All CRUD endpoints publicly accessible; login returns token but nothing validates it.
Impact: Anyone can create admin users, read/modify all data.
Recommendation: Implement JWT or session-based auth with decorators.

### [CRITICAL] Weak Password Hashing (MD5, no salt)
File: models/user.py:27-32
Description: Passwords hashed with unsalted MD5 via hashlib.md5().
Impact: Rainbow tables make stored passwords trivial to recover.
Recommendation: Use werkzeug.security generate_password_hash / check_password_hash.

### [CRITICAL] Password Hash Exposed in API Responses
File: models/user.py:16-25; routes/user_routes.py:33,85,129,207
Description: User.to_dict() includes password field returned by create, update, get, login.
Impact: Attackers obtain hashes directly from API for offline cracking.
Recommendation: Remove password from all serialization.

### [CRITICAL] Hardcoded Secrets and SMTP Credentials
File: app.py:13; services/notification_service.py:7-10
Description: SECRET_KEY and SMTP credentials embedded in source code.
Impact: Secrets in version control; session forgery risk.
Recommendation: Load from environment variables via config/settings.py.

### [CRITICAL] Fake Predictable Authentication Token
File: routes/user_routes.py:207-211
Description: Login returns fake-jwt-token-{id} with no signing or verification.
Impact: Trivial impersonation; false sense of security.
Recommendation: Issue signed JWTs with expiration.

### [HIGH] Fat Controllers / Broken Layered Architecture
File: routes/task_routes.py; routes/user_routes.py; routes/report_routes.py
Description: Routes perform validation, ORM queries, and business rules inline; services unused.
Impact: Hard to test; services/ and utils/ folders are dead weight.
Recommendation: Introduce service classes; keep routes as thin HTTP adapters.

### [HIGH] Category CRUD Misplaced in Reports Blueprint
File: routes/report_routes.py:157-223
Description: Category endpoints live under report_bp instead of dedicated module.
Impact: Violates cohesion and discoverability.
Recommendation: Move to category_routes.py.

### [HIGH] Privilege Escalation via Unauthenticated Role Assignment
File: routes/user_routes.py:52,71-78,119-122
Description: POST/PUT /users accept role (admin/manager) without caller authorization.
Impact: Anonymous clients can promote themselves to admin.
Recommendation: Restrict role changes to authenticated admins.

### [MEDIUM] N+1 Query in Task Listing
File: routes/task_routes.py:14-57
Description: GET /tasks loads all tasks then User.query.get() and Category.query.get() per task.
Impact: Performance degrades linearly with task count.
Recommendation: Use joinedload or single query with joins.

### [MEDIUM] Duplicated Overdue Calculation Logic
File: models/task.py:50-60 (unused); routes/task_routes.py, user_routes.py, report_routes.py
Description: Same overdue conditional copy-pasted 5+ times; model method ignored.
Impact: Inconsistent behavior if logic changes in one place.
Recommendation: Centralize in Task.is_overdue().

### [MEDIUM] Production-Unsafe Runtime Configuration
File: app.py:15,30-31,34
Description: CORS(app) allows all origins; debug=True; db.create_all() at import.
Impact: Debug exposes stack traces; open CORS enables abuse.
Recommendation: Environment-based config; app factory pattern.

### [MEDIUM] Bare except Clauses
File: routes/user_routes.py:130; routes/task_routes.py:62
Description: Multiple bare except blocks return generic 500s without structured logging.
Impact: Debugging difficult; bugs surface as opaque failures.
Recommendation: Catch specific exceptions; use global error handler.

### [MEDIUM] Inefficient Aggregate Queries in Reports
File: routes/report_routes.py:24-68
Description: Summary runs 9+ separate COUNT queries plus Python loops over all tasks/users.
Impact: Poor scalability as data grows.
Recommendation: Use SQL GROUP BY and conditional aggregates.

### [LOW] Dead Code and Unused Dependencies
File: app.py:7; requirements.txt (marshmallow, requests, python-dotenv unused)
Description: Orphaned helpers and notification service never imported.
Impact: Confusing codebase; bloated dependencies.
Recommendation: Wire up or remove dead modules.

================================
Total: 14 findings
================================

Phase 2 complete. Proceed with refactoring (Phase 3)? [y/n]
