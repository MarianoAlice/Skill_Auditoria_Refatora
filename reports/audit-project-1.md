================================
ARCHITECTURE AUDIT REPORT
================================
Project: code-smells-project
Stack:   Python + Flask
Files:   4 analyzed | ~580 lines of code

## Summary
CRITICAL: 5 | HIGH: 4 | MEDIUM: 3 | LOW: 2

## Findings

### [CRITICAL] SQL Injection via String Concatenation
File: models.py:28,47-49,58-60,68,92,109-110,127-128,140,155,158-165,174,188,220,224,280,291-293
Description: Nearly all SQL queries concatenate user-controlled input instead of using parameterized placeholders.
Impact: Attackers can inject SQL to bypass authentication, exfiltrate or corrupt data.
Recommendation: Replace all string-built queries with parameterized statements (? placeholders).

### [CRITICAL] Unauthenticated Arbitrary SQL Execution
File: app.py:59-78
Description: POST /admin/query accepts arbitrary SQL from request body and executes it without authentication.
Impact: Full database compromise — any client can read, modify or delete all data.
Recommendation: Remove this endpoint entirely.

### [CRITICAL] Plaintext Password Storage and Exposure
File: models.py:72-87,89-103; controllers.py:128-134; database.py:75-82
Description: Passwords stored in plaintext; get_todos_usuarios() returns senha field in API responses.
Impact: Credential theft if database or API is compromised.
Recommendation: Hash passwords with werkzeug/bcrypt; never return password fields in responses.

### [CRITICAL] Hardcoded Secret Key Exposed via Health Endpoint
File: app.py:7-8; controllers.py:286-289
Description: SECRET_KEY hardcoded as 'minha-chave-super-secreta-123' and exposed in GET /health response.
Impact: Session forgery and configuration disclosure to any caller.
Recommendation: Load secrets from environment; health endpoint returns only non-sensitive status.

### [CRITICAL] Unauthenticated Database Reset
File: app.py:47-57
Description: POST /admin/reset-db wipes all tables without authentication.
Impact: Total data loss and denial of service by any anonymous client.
Recommendation: Remove endpoint or protect with admin auth and environment guards.

### [HIGH] God Class — models.py Contains All Domain Logic
File: models.py:1-314
Description: Single file contains SQL, business rules, order creation, and sales report logic for 4 domains.
Impact: Impossible to test in isolation; any change affects entire application.
Recommendation: Split into models per domain (produto, usuario, pedido).

### [HIGH] No Authentication or Authorization
File: app.py:11-30; controllers.py (all handlers)
Description: No JWT, session, or role checks on sensitive endpoints like GET /usuarios, GET /pedidos, PUT /pedidos/status.
Impact: Anyone can list users with passwords, view orders, and change order status.
Recommendation: Implement authentication middleware with role-based access control.

### [HIGH] Business Logic and Side Effects in Controllers
File: controllers.py:208-210,247-250
Description: Controllers contain notification side effects via print() instead of a service layer.
Impact: Violates SRP; side effects cannot be mocked or swapped in tests.
Recommendation: Extract notification logic to services/pedido_service.py.

### [HIGH] Global Singleton Database Connection
File: database.py:4-11
Description: Single global db_connection shared across all requests with check_same_thread=False.
Impact: Race conditions and SQLite lock issues under concurrent load.
Recommendation: Use Flask g object for per-request connections.

### [MEDIUM] N+1 Query Problem in Order Listing
File: models.py:171-233
Description: Separate queries for items and product names inside nested loops per order.
Impact: Performance degrades linearly with order count.
Recommendation: Use JOINs to fetch orders with items in a single query.

### [MEDIUM] Debug Mode and Permissive CORS
File: app.py:7-9,88
Description: DEBUG=True, CORS(app) with no origin restrictions, debug=True in production health response.
Impact: Debug exposes stack traces; open CORS enables cross-origin abuse.
Recommendation: Load config from environment; separate dev/prod settings.

### [MEDIUM] Broad Exception Handling Exposes Internal Errors
File: controllers.py (throughout)
Description: Generic Exception caught and str(e) returned to clients.
Impact: Leaks SQL errors and internal paths to attackers.
Recommendation: Register centralized error handlers; return generic messages.

### [LOW] Magic Numbers in Sales Report Discount Logic
File: models.py:256-262
Description: Discount thresholds (1000, 5000, 10000) and rates (0.02, 0.05, 0.1) hardcoded inline.
Impact: Business rules opaque and hard to change.
Recommendation: Extract to named constants in config/settings.py.

### [LOW] Print-Based Logging
File: controllers.py:8,11,57,106,161,179,208-210,247-250
Description: Application uses print() for logging and notifications.
Impact: No log levels, no rotation, unsuitable for production observability.
Recommendation: Use Python logging module with configurable handlers.

================================
Total: 14 findings
================================

Phase 2 complete. Proceed with refactoring (Phase 3)? [y/n]
