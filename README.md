# Skill Auditoria Refatora — Refatoração Arquitetural Automatizada

Skill `refactor-arch` para auditar e refatorar projetos legados para o padrão MVC, usando **Gemini CLI** (`.gemini/skills/refactor-arch/`).

Repositório: [github.com/MarianoAlice/Skill_Auditoria_Refatora](https://github.com/MarianoAlice/Skill_Auditoria_Refatora)

## Estrutura

```
Skill_Auditoria_Refatora/
├── README.md
├── reports/
│   ├── audit-project-1.md
│   ├── audit-project-2.md
│   └── audit-project-3.md
├── code-smells-project/      # Python/Flask — E-commerce
├── ecommerce-api-legacy/     # Node.js/Express — LMS
└── task-manager-api/         # Python/Flask — Task Manager
```

---

## A) Análise Manual

### Projeto 1 — `code-smells-project` (Python/Flask — E-commerce)

| Sev | Problema | Arquivo | Justificativa |
|-----|----------|---------|---------------|
| CRITICAL | SQL Injection por concatenação | `models.py` (múltiplas linhas) | Input do usuário embutido diretamente em queries SQL permite bypass de autenticação e exfiltração de dados |
| CRITICAL | Endpoint `/admin/query` sem auth | `app.py:59-78` | Qualquer cliente pode executar SQL arbitrário — comprometimento total do banco |
| CRITICAL | Senhas em plaintext na API | `models.py`, `controllers.py` | Credenciais expostas violam OWASP e LGPD |
| CRITICAL | SECRET_KEY hardcoded e exposta | `app.py:7-8`, `controllers.py:286-289` | Chave retornada em `/health` permite forjar sessões |
| HIGH | God Class em `models.py` | `models.py:1-314` | SQL + regras de negócio de 4 domínios no mesmo arquivo impede testes isolados |
| HIGH | Sem autenticação/autorização | `app.py`, `controllers.py` | Endpoints sensíveis (usuários, pedidos, relatórios) totalmente públicos |
| MEDIUM | N+1 queries em pedidos | `models.py:171-233` | Query dentro de loop degrada performance linearmente |
| MEDIUM | Debug=True + CORS aberto | `app.py:7-9, 88` | Stack traces e CORS permissivo em ambiente declarado como produção |
| LOW | Magic numbers em descontos | `models.py:256-262` | Regras de negócio opacas e difíceis de manter |
| LOW | `print()` em vez de logging | `controllers.py` | Sem níveis de log, inadequado para produção |

### Projeto 2 — `ecommerce-api-legacy` (Node.js/Express — LMS)

| Sev | Problema | Arquivo | Justificativa |
|-----|----------|---------|---------------|
| CRITICAL | Credenciais hardcoded | `src/utils.js:1-7` | Chaves de pagamento e DB no código-fonte |
| CRITICAL | God Class `AppManager` | `src/AppManager.js` | DB + rotas + checkout + relatório em uma classe |
| CRITICAL | Cartão logado no console | `src/AppManager.js:45` | Violação PCI-DSS |
| CRITICAL | `badCrypto()` — hash falso | `src/utils.js:17-23` | Senhas trivialmente reversíveis |
| CRITICAL | Admin sem autenticação | `src/AppManager.js:80-129` | Relatório financeiro e PII públicos |
| HIGH | Lógica de checkout inline | `src/AppManager.js:28-78` | Impossível testar sem HTTP |
| HIGH | Callback hell | `src/AppManager.js` | 5-6 níveis de aninhamento, propenso a erros |
| MEDIUM | N+1 no relatório financeiro | `src/AppManager.js:89-127` | Milhares de queries sob carga |
| MEDIUM | SQLite `:memory:` | `src/AppManager.js:7` | Dados perdidos a cada restart |
| LOW | Nomes crípticos (`usr`, `eml`) | `src/AppManager.js:29-33` | Prejudica legibilidade e onboarding |

### Projeto 3 — `task-manager-api` (Python/Flask — Task Manager)

| Sev | Problema | Arquivo | Justificativa |
|-----|----------|---------|---------------|
| CRITICAL | Sem auth real nos endpoints | `routes/*.py` | Qualquer um pode CRUD em todos os dados |
| CRITICAL | MD5 sem salt | `models/user.py:27-32` | Hash fraco, rainbow tables |
| CRITICAL | Hash exposto em `to_dict()` | `models/user.py:16-25` | API retorna hash para cracking offline |
| CRITICAL | SECRET_KEY e SMTP hardcoded | `app.py:13`, `services/notification_service.py` | Segredos no repositório |
| HIGH | Fat controllers | `routes/task_routes.py` etc. | Lógica de negócio presa nas rotas |
| HIGH | Services não utilizados | `services/`, `utils/` | Camada morta — falsa sensação de arquitetura |
| MEDIUM | N+1 em listagem de tasks | `routes/task_routes.py:14-57` | Query por task para user/category |
| MEDIUM | Overdue duplicado 5+ vezes | `routes/*.py` | Viola DRY; método do model ignorado |
| MEDIUM | CORS aberto + debug | `app.py` | Config insegura para produção |
| LOW | Imports e deps mortas | vários arquivos | Código confuso, dependências não usadas |

---

## B) Construção da Skill

### Decisões de design

- **Ferramenta:** Gemini CLI com skill em `.gemini/skills/refactor-arch/` (equivalente ao `.claude/skills/` do curso)
- **SKILL.md** orquestra 3 fases sequenciais; conhecimento de domínio em `references/` (progressive disclosure)
- **Scripts opcionais:** `detect_stack.py` e `validate_endpoints.py` para tarefas determinísticas

### Anti-patterns no catálogo (12 total)

| ID | Anti-pattern | Severidade |
|----|-------------|------------|
| AP01 | God Class / God Method | CRITICAL |
| AP02 | SQL Injection | CRITICAL |
| AP03 | Hardcoded Secrets | CRITICAL |
| AP04 | Plaintext/Weak Password Hash | CRITICAL |
| AP05 | Missing Auth/Authorization | HIGH |
| AP06 | Fat Controller / Business in Routes | HIGH |
| AP07 | N+1 Queries | MEDIUM |
| AP08 | Global Mutable State | HIGH |
| AP09 | Duplicated Validation Logic | MEDIUM |
| AP10 | Deprecated APIs | MEDIUM |
| AP11 | Magic Numbers | LOW |
| AP12 | Print-based Logging | LOW |

### Agnosticismo tecnológico

- Heurísticas baseadas em extensões de arquivo e manifestos (`package.json`, `requirements.txt`)
- Sinais de detecção **sintáticos** (concatenação SQL, `md5`, `global`) — não nomes de arquivo específicos
- Playbook com exemplos em **Python e JavaScript**
- Guidelines MVC mapeiam camadas para Flask e Express

### Desafios

- Projeto 3 já tinha estrutura parcial — skill distingue "melhorar camadas" vs "criar do zero"
- Adaptação Claude Code → Gemini CLI: path `.gemini/skills/`, comando via prompt ou match na `description`

---

## C) Resultados

### Findings por projeto (Fase 2)

| Projeto | CRITICAL | HIGH | MEDIUM | LOW | Total |
|---------|----------|------|--------|-----|-------|
| code-smells-project | 5 | 4 | 3 | 2 | 14 |
| ecommerce-api-legacy | 5 | 4 | 3 | 2 | 14 |
| task-manager-api | 5 | 3 | 5 | 1 | 14 |

### Antes / Depois

**code-smells-project:**
```
ANTES: app.py, controllers.py, models.py, database.py (monolito)
DEPOIS: config/, database/, models/, controllers/, views/, services/, middlewares/, app.py
```

**ecommerce-api-legacy:**
```
ANTES: app.js, AppManager.js, utils.js (God Class)
DEPOIS: config/, models/, services/, controllers/, routes/, middlewares/, app.js
```

**task-manager-api:**
```
ANTES: routes com lógica inline; services mortos; categories em report_bp
DEPOIS: config/, services/ ativos, routes finos, category_routes.py, middlewares/
```

### Checklist de Validação

#### Projeto 1 — code-smells-project
- [x] Linguagem detectada: Python
- [x] Framework detectado: Flask 3.1.1
- [x] Domínio: E-commerce API
- [x] ≥5 findings (14)
- [x] ≥1 CRITICAL/HIGH
- [x] MVC structure + config + error handler
- [x] App inicia: `health 200`, `produtos 200`, `login 200`

#### Projeto 2 — ecommerce-api-legacy
- [x] Linguagem: JavaScript
- [x] Framework: Express 4.18.2
- [x] Domínio: LMS API com checkout
- [x] ≥5 findings (14)
- [x] Checkout service: `checkout ok { msg: 'Sucesso', enrollment_id: 2 }`

#### Projeto 3 — task-manager-api
- [x] Linguagem: Python / Flask
- [x] Domínio: Task Manager
- [x] ≥5 findings (14)
- [x] `health 200`, `tasks 200`

---

## D) Como Executar

### Pré-requisitos

- [Gemini CLI](https://geminicli.com/docs/cli/skills/) instalado
- Python 3.x (projetos Flask)
- Node.js 18+ (projeto Express)

### Invocar a skill

```powershell
cd code-smells-project
gemini
# Na sessão interativa:
/skills list
/trust                    # se workspace skill não aparecer
# Prompt: "Execute a skill refactor-arch neste projeto"
```

Repetir copiando `.gemini/skills/refactor-arch/` para os outros projetos.

> **Nota:** O curso usa `claude "/refactor-arch"` com `.claude/skills/`. Este projeto adapta para Gemini CLI com `.gemini/skills/`.

### Validar refatoração

**Flask:**
```powershell
pip install -r requirements.txt
python app.py
python .gemini/skills/refactor-arch/scripts/validate_endpoints.py http://localhost:5000
```

**Express:**
```powershell
npm install
npm start
# Testar endpoints em api.http
```

### Relatórios

Saída da Fase 2 salva em:
- `reports/audit-project-1.md`
- `reports/audit-project-2.md`
- `reports/audit-project-3.md`

---

## Referências

- [Gemini CLI — Agent Skills](https://geminicli.com/docs/cli/skills/)
- [Critérios do desafio](criterios.txt)
- Fork base: `mba-ia-refactor-projects-skill`
