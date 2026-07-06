# Refactoring Playbook

Eight transformation patterns with before/after examples.

---

## T01 — Monolith to MVC Directory Structure

**Before (Python):**
```
app.py          # routes + admin endpoints
controllers.py  # HTTP + validation
models.py       # SQL + business rules
database.py
```

**After:**
```
app.py
config/settings.py
database/connection.py
models/produto_model.py
controllers/produto_controller.py
views/routes.py
middlewares/error_handler.py
```

---

## T02 — SQL Concatenation to Parameterized Queries

**Before:**
```python
cursor.execute("SELECT * FROM produtos WHERE id = " + str(id))
cursor.execute("WHERE email = '" + email + "' AND senha = '" + senha + "'")
```

**After:**
```python
cursor.execute("SELECT * FROM produtos WHERE id = ?", (id,))
cursor.execute("SELECT * FROM usuarios WHERE email = ? AND senha = ?", (email, senha_hash))
```

---

## T03 — Hardcoded Secrets to Environment Config

**Before:**
```python
app.config["SECRET_KEY"] = "minha-chave-super-secreta-123"
```

```javascript
const config = { paymentGatewayKey: "pk_live_1234567890abcdef" };
```

**After:**
```python
# config/settings.py
import os
SECRET_KEY = os.environ.get("SECRET_KEY", "dev-only-key")
```

```javascript
// config/settings.js
module.exports = {
  paymentGatewayKey: process.env.PAYMENT_GATEWAY_KEY || '',
  port: parseInt(process.env.PORT || '3000', 10),
};
```

---

## T04 — God Class to Domain Split

**Before:**
```javascript
class AppManager {
  initDb() { /* schema + seed */ }
  setupRoutes(app) { /* checkout + report + delete */ }
}
```

**After:**
```javascript
// models/database.js — schema init
// services/checkoutService.js — checkout logic
// controllers/checkoutController.js — HTTP adapter
// routes/checkoutRoutes.js — route wiring
```

---

## T05 — Fat Routes to Thin Controller + Service

**Before:**
```python
@task_bp.route('/tasks', methods=['GET'])
def list_tasks():
    tasks = Task.query.all()
    result = []
    for task in tasks:
        user = User.query.get(task.user_id)  # N+1
        # ... 40 more lines
```

**After:**
```python
# controllers/task_controller.py
def list_tasks():
    return jsonify(task_service.list_all()), 200

# services/task_service.py
def list_all():
    return [t.to_dict() for t in Task.query.options(joinedload(Task.user)).all()]
```

---

## T06 — Callback Hell to Async/Await

**Before:**
```javascript
db.get("SELECT ...", [id], (err, row) => {
  db.run("INSERT ...", [], function(err) {
    db.run("INSERT ...", [], (err) => { res.json(...); });
  });
});
```

**After:**
```javascript
const row = await db.get("SELECT ...", [id]);
const enrId = await db.run("INSERT ...", []);
await db.run("INSERT ...", []);
res.json({ msg: "Sucesso", enrollment_id: enrId });
```

---

## T07 — N+1 to JOIN / Eager Load

**Before:**
```python
for row in pedidos:
    cursor2.execute("SELECT * FROM itens_pedido WHERE pedido_id = " + str(row["id"]))
```

**After:**
```python
cursor.execute("""
    SELECT p.*, i.produto_id, i.quantidade, pr.nome as produto_nome
    FROM pedidos p
    LEFT JOIN itens_pedido i ON i.pedido_id = p.id
    LEFT JOIN produtos pr ON pr.id = i.produto_id
    WHERE p.usuario_id = ?
""", (usuario_id,))
```

---

## T08 — Scattered Errors to Centralized Handler

**Before:**
```python
except Exception as e:
    return jsonify({"erro": str(e)}), 500  # in every handler
```

**After:**
```python
# middlewares/error_handler.py
def register_error_handlers(app):
    @app.errorhandler(Exception)
    def handle_error(e):
        app.logger.exception(e)
        return jsonify({"erro": "Erro interno do servidor"}), 500
```

```javascript
// middlewares/errorHandler.js
module.exports = (err, req, res, next) => {
  console.error(err.message);
  res.status(500).json({ error: 'Erro interno do servidor' });
};
```

---

## T09 — Weak Password Hash to bcrypt/werkzeug

**Before:**
```python
self.password = hashlib.md5(pwd.encode()).hexdigest()
```

**After:**
```python
from werkzeug.security import generate_password_hash, check_password_hash
self.password = generate_password_hash(pwd)
```

---

## T10 — Dead Service Layer to Wired Services

**Before:** `services/notification_service.py` exists but never imported

**After:**
```python
# services/task_service.py used by controllers
from services.notification_service import NotificationService
notification_service = NotificationService()
notification_service.send_task_created(task)
```

Or remove unused modules if out of scope.

---

## Refactoring Order

1. Security fixes (secrets, SQL injection, remove dangerous endpoints)
2. Config extraction
3. Split models (parameterized queries)
4. Extract services
5. Thin controllers + route registration
6. Centralize error handling
7. Validate boot + endpoints
