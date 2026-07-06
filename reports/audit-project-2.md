================================
ARCHITECTURE AUDIT REPORT
================================
Project: ecommerce-api-legacy
Stack:   JavaScript + Express
Files:   3 analyzed | ~182 lines of code

## Summary
CRITICAL: 5 | HIGH: 4 | MEDIUM: 3 | LOW: 2

## Findings

### [CRITICAL] Hardcoded Production Credentials
File: src/utils.js:1-7
Description: Database credentials, payment gateway live key, and SMTP user hardcoded in source.
Impact: Secrets exposed to anyone with repo access; violates secret-management best practices.
Recommendation: Move all secrets to environment variables.

### [CRITICAL] God Class — AppManager
File: src/AppManager.js:4-141
Description: AppManager handles schema, seeding, routing, checkout, payments, reports, and user deletion in one class.
Impact: Impossible to unit test in isolation; violates SRP and MVC entirely.
Recommendation: Split into models/, controllers/, routes/, services/.

### [CRITICAL] Credit Card and Payment Key Logged
File: src/AppManager.js:45
Description: Checkout logs full card number and payment gateway key to console.
Impact: PCI-DSS violation; PAN and secrets may end up in logs.
Recommendation: Never log PAN or secrets; mask card data.

### [CRITICAL] Broken Password Hashing (badCrypto)
File: src/utils.js:17-23; AppManager.js:68
Description: badCrypto() base64-encodes password in a loop; seed password is plaintext '123'.
Impact: Passwords trivially guessable; accounts easily compromised.
Recommendation: Use crypto.scrypt or bcrypt with per-user salt.

### [CRITICAL] Unauthenticated Admin Endpoint
File: src/AppManager.js:80-129
Description: GET /api/admin/financial-report exposes revenue and PII without authentication.
Impact: Any anonymous client can access sensitive financial data.
Recommendation: Add JWT/session auth and role-based access control.

### [HIGH] Business Logic in Route Handlers
File: src/AppManager.js:28-78
Description: Entire checkout flow lives inline in Express route callback.
Impact: Logic cannot be reused or tested without HTTP.
Recommendation: Extract CheckoutService and CheckoutController.

### [HIGH] Callback Hell (Pyramid of Doom)
File: src/AppManager.js:37-77,89-127
Description: Up to 5-6 levels of nested db.get/db.run callbacks.
Impact: Hard to read, error-prone, difficult to add transactions.
Recommendation: Use async/await with promisified database wrapper.

### [HIGH] N+1 Query Pattern in Financial Report
File: src/AppManager.js:89-127
Description: Separate queries per course, enrollment, user, and payment in nested loops.
Impact: Performance degrades linearly with data volume.
Recommendation: Replace with JOINs in a single aggregated query.

### [HIGH] Global Mutable State
File: src/utils.js:9-10,25
Description: Module-level globalCache and totalRevenue exported as mutable shared state.
Impact: Hidden coupling and untestable side effects.
Recommendation: Replace with injectable cache service or remove.

### [MEDIUM] In-Memory Database — No Persistence
File: src/AppManager.js:7
Description: sqlite3.Database(':memory:') — all data lost on restart.
Impact: Unsuitable for production; enrollments vanish after deploy.
Recommendation: Use file-based SQLite path from config.

### [MEDIUM] Orphan Records on User Deletion
File: src/AppManager.js:131-137
Description: DELETE FROM users does not cascade to enrollments or payments.
Impact: Data integrity violations; incomplete GDPR erasure.
Recommendation: Transactional cleanup across related tables.

### [MEDIUM] No Centralized Error Handling
File: src/app.js:5-14; AppManager.js scattered res.status(500)
Description: No global error handler; ad-hoc error strings.
Impact: Inconsistent API responses; missing standard security headers.
Recommendation: Add middlewares/errorHandler.js with consistent JSON errors.

### [LOW] Cryptic Variable Names
File: src/AppManager.js:29-33
Description: Request fields use opaque names: usr, eml, pwd, c_id, cc.
Impact: Hurts readability and API discoverability.
Recommendation: Use descriptive names in controllers while preserving API contract.

### [LOW] Magic Numbers in badCrypto Loop
File: src/utils.js:19-22
Description: 10000 loop iterations and substring(0, 10) with no named constants.
Impact: Obscures intent; signals copy-paste design.
Recommendation: Remove badCrypto; use standard crypto libraries.

================================
Total: 14 findings
================================

Phase 2 complete. Proceed with refactoring (Phase 3)? [y/n]
