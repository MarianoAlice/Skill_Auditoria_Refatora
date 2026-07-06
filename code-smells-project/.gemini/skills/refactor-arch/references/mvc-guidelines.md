# MVC Target Architecture Guidelines

## Layer Responsibilities

### Models
- Data access only: queries, ORM mappings, serialization helpers
- No HTTP request/response handling
- No business orchestration across multiple entities
- Parameterized queries only; never concatenate user input into SQL

### Views / Routes
- Route registration and HTTP method mapping only
- Delegate immediately to controllers
- Flask: `views/routes.py` or Blueprint registration in `app.py`
- Express: `routes/*.js` importing controller methods

### Controllers
- Parse request input, call services/models, return HTTP response
- Thin: no raw SQL, no complex business rules
- Validate input via schemas or dedicated validators

### Services (recommended for business logic)
- Order creation, checkout flow, report aggregation
- Callable without HTTP context (testable)

### Config
- `config/settings.py` (Python) or `config/settings.js` (Node)
- Load from environment variables with safe defaults for dev
- Never hardcode secrets

### Middlewares
- Centralized error handling
- Auth middleware for protected routes
- CORS, logging configured per environment

### Entry Point (Composition Root)
- `app.py` or `src/app.js` wires config, database, routes, middlewares
- Minimal logic

## Target Directory Structure

### Python/Flask
```
project/
├── app.py
├── config/settings.py
├── database/connection.py
├── models/
├── controllers/
├── views/routes.py
├── services/          (optional)
└── middlewares/error_handler.py
```

### Node/Express
```
src/
├── app.js
├── config/settings.js
├── models/
├── controllers/
├── routes/
├── services/
└── middlewares/errorHandler.js
```

## Partially Organized Projects

When project already has `models/`, `routes/`, `services/`:
- Move business logic from routes into services
- Wire unused services or remove dead code
- Fix security issues regardless of existing structure
- Do not break existing URL paths

## Validation Checklist (Phase 3)

- [ ] Config module without hardcoded secrets
- [ ] Models abstract data access
- [ ] Routes/views separate from business logic
- [ ] Controllers are thin
- [ ] Error handler centralized
- [ ] App boots without errors
- [ ] Original endpoints respond correctly
