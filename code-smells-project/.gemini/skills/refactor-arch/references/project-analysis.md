# Project Analysis Heuristics

## Language Detection

| Signal | Language |
|--------|----------|
| `*.py`, `requirements.txt`, `pyproject.toml` | Python |
| `*.js`, `*.ts`, `package.json` | JavaScript/TypeScript |
| `*.go`, `go.mod` | Go |
| `*.java`, `pom.xml`, `build.gradle` | Java |

## Framework Detection

### Python
- `from flask import` or `Flask(` → Flask
- `from fastapi import` → FastAPI
- `django` in requirements → Django

### JavaScript
- `express()` or `require('express')` → Express
- `fastify` → Fastify
- `@nestjs` → NestJS

Read version from `requirements.txt` or `package.json` dependencies.

## Database Detection

| Signal | Database |
|--------|----------|
| `sqlite3`, `sqlite:///` | SQLite |
| `psycopg2`, `postgresql://` | PostgreSQL |
| `mysql`, `mysql://` | MySQL |
| `:memory:` in sqlite connect | In-memory SQLite |
| `mongoose`, `mongodb://` | MongoDB |

Parse `CREATE TABLE` statements and model classes for table names.

## Architecture Mapping

Classify current architecture:

1. **Monolithic flat** — few files, mixed concerns (routes + DB + logic in same file)
2. **Pseudo-MVC** — files named models/controllers but logic misplaced
3. **Partial layering** — models/routes/services exist but routes own business logic
4. **MVC-compliant** — clear separation with thin controllers

### Heuristics

- Count source files (exclude tests, node_modules, __pycache__)
- Locate entry point: `app.py`, `src/app.js`, `main.py`
- Check if routes are inline in entry file vs separate module
- Check if models contain HTTP or validation logic
- Estimate LOC per file; flag files >250 LOC as potential God Class

## Domain Inference

Infer domain from:
- Table/entity names (produtos, pedidos, tasks, courses)
- Route prefixes (`/api/checkout`, `/produtos`)
- README if present

## Phase 1 Output Format

```
================================
PHASE 1: PROJECT ANALYSIS
================================
Language:      <language>
Framework:     <framework> <version>
Dependencies:  <key deps>
Domain:        <domain description>
Architecture:  <classification>
Source files:  <N> files analyzed
DB tables:     <table list>
================================
```
