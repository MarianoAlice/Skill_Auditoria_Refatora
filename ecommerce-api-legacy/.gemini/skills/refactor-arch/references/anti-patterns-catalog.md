# Anti-Patterns Catalog

Severity scale: CRITICAL | HIGH | MEDIUM | LOW

---

## AP01 — God Class / God Method (CRITICAL)

**Signals:**
- Single file/class >250 LOC handling DB schema, routes, business logic, and reporting
- Class name like `AppManager`, `GodManager` owning entire application
- One module imports express/flask AND runs SQL AND defines routes

**Examples:** `AppManager.js` with initDb + setupRoutes + checkout + reports

**Recommendation:** Split by domain into models, controllers, routes, services

---

## AP02 — SQL Injection (CRITICAL)

**Signals:**
- String concatenation in SQL: `"WHERE id = " + str(id)`, `f"SELECT ... {var}"`
- User input embedded in query without `?` placeholders
- Admin endpoint executing raw SQL from request body

**Recommendation:** Parameterized queries; remove arbitrary SQL endpoints

---

## AP03 — Hardcoded Secrets (CRITICAL)

**Signals:**
- `SECRET_KEY = '...'`, `api_key`, `dbPass`, `paymentGatewayKey` in source
- Secrets returned in API responses (`/health` exposing secret_key)

**Recommendation:** `os.environ` / `process.env`; never expose in responses

---

## AP04 — Plaintext / Weak Password Hash (CRITICAL)

**Signals:**
- Passwords stored/compared as plaintext in SQL
- `hashlib.md5`, custom `badCrypto()` base64 loops
- Seed passwords like `'123'`, `'admin123'`

**Recommendation:** bcrypt, argon2, or werkzeug `generate_password_hash`

---

## AP05 — Missing Auth / Authorization (HIGH)

**Signals:**
- `/admin/*` routes without middleware
- CRUD on users/orders/financial data publicly accessible
- Login returns token but no validation on subsequent requests

**Recommendation:** JWT/session middleware; role-based access control

---

## AP06 — Fat Controller / Business in Routes (HIGH)

**Signals:**
- Route handler >50 lines with validation + DB + business rules
- `print("ENVIANDO EMAIL")` side effects in controllers
- ORM queries and aggregation inside Flask Blueprint handlers

**Recommendation:** Extract services; keep controllers thin

---

## AP07 — N+1 Queries (MEDIUM)

**Signals:**
- `for row in rows:` followed by new `cursor.execute` per iteration
- `forEach` with nested `db.get` / `db.all` callbacks per item
- `User.query.get()` inside loop over tasks

**Recommendation:** JOINs, eager loading (`joinedload`), single aggregated query

---

## AP08 — Global Mutable State (HIGH)

**Signals:**
- Module-level `globalCache`, `totalRevenue`, `db_connection = None`
- `global db_connection` shared across requests

**Recommendation:** Request-scoped connections (Flask `g`), injectable services

---

## AP09 — Duplicated Validation Logic (MEDIUM)

**Signals:**
- Same if-blocks in create and update handlers
- Overdue calculation copy-pasted in 5+ route files
- Category whitelist checked in one endpoint but not another

**Recommendation:** Shared validator functions or schema library (marshmallow, Joi)

---

## AP10 — Deprecated / Unsafe APIs (MEDIUM)

**Signals:**
- `hashlib.md5()` for password hashing (deprecated for security)
- `sqlite3` nested callbacks without promisify (legacy Node pattern)
- `app.run(debug=True)` with `host='0.0.0.0'` in production config
- `db.create_all()` at import time
- Fake tokens: `'fake-jwt-token-' + str(user.id)`

**Recommendation:** Modern crypto, async/await, app factory pattern, real JWT

---

## AP11 — Magic Numbers (LOW)

**Signals:**
- Numeric literals in business rules: `if faturamento > 10000`, `0.1` discount
- Loop count `10000` in crypto with no named constant

**Recommendation:** Named constants in config or domain module

---

## AP12 — Print-Based Logging (LOW)

**Signals:**
- `print("ERRO: ...")`, `console.log(cardNumber)` for errors/notifications
- No `logging` module or structured logger

**Recommendation:** Python `logging` / Winston; never log PAN or secrets

---

## Detection Workflow

1. Grep for patterns: `SECRET_KEY`, `md5`, `+ str(`, `console.log`, `global `
2. Measure file LOC; inspect largest files first
3. Trace route handlers for SQL and business logic
4. Check health/debug endpoints for information disclosure
5. Verify auth middleware on sensitive routes
