================================
RELATÓRIO DE AUDITORIA DE ARQUITETURA
================================
Projeto: task-manager-api
Stack:   Python + Flask
Arquivos: 15 analisados | ~1200 linhas de código

## Resumo
CRÍTICO: 5 | ALTO: 3 | MÉDIO: 5 | BAIXO: 1

## Achados

### [CRÍTICO] Ausência de Autenticação nos Endpoints da API
Arquivo: routes/user_routes.py:10-211; routes/task_routes.py:11-299
Descrição: Todos os endpoints CRUD são publicamente acessíveis; login retorna token mas nada o valida.
Impacto: Qualquer pessoa pode criar usuários admin, ler e modificar todos os dados.
Recomendação: Implementar autenticação JWT ou baseada em sessão com decorators.

### [CRÍTICO] Hash de Senha Fraco (MD5, sem salt)
Arquivo: models/user.py:27-32
Descrição: Senhas hasheadas com MD5 sem salt via hashlib.md5().
Impacto: Rainbow tables tornam senhas armazenadas trivialmente recuperáveis.
Recomendação: Usar werkzeug.security generate_password_hash / check_password_hash.

### [CRÍTICO] Hash de Senha Exposto nas Respostas da API
Arquivo: models/user.py:16-25; routes/user_routes.py:33,85,129,207
Descrição: User.to_dict() inclui campo password retornado por create, update, get e login.
Impacto: Atacantes obtêm hashes diretamente da API para cracking offline.
Recomendação: Remover password de toda serialização.

### [CRÍTICO] Segredos e Credenciais SMTP Hardcoded
Arquivo: app.py:13; services/notification_service.py:7-10
Descrição: SECRET_KEY e credenciais SMTP embutidas no código-fonte.
Impacto: Segredos no controle de versão; risco de falsificação de sessão.
Recomendação: Carregar de variáveis de ambiente via config/settings.py.

### [CRÍTICO] Token de Autenticação Falso e Previsível
Arquivo: routes/user_routes.py:207-211
Descrição: Login retorna fake-jwt-token-{id} sem assinatura ou verificação.
Impacto: Impersonação trivial; falsa sensação de segurança.
Recomendação: Emitir JWTs assinados com expiração.

### [ALTO] Fat Controllers / Arquitetura em Camadas Quebrada
Arquivo: routes/task_routes.py; routes/user_routes.py; routes/report_routes.py
Descrição: Rotas executam validação, queries ORM e regras de negócio inline; services não utilizados.
Impacto: Difícil de testar; pastas services/ e utils/ são peso morto.
Recomendação: Introduzir classes de serviço; manter rotas como adaptadores HTTP finos.

### [ALTO] CRUD de Categorias no Blueprint de Relatórios
Arquivo: routes/report_routes.py:157-223
Descrição: Endpoints de categorias vivem sob report_bp em vez de módulo dedicado.
Impacto: Viola coesão e descoberta do código.
Recomendação: Mover para category_routes.py.

### [ALTO] Escalação de Privilégio via Atribuição de Papel sem Autenticação
Arquivo: routes/user_routes.py:52,71-78,119-122
Descrição: POST/PUT /users aceitam role (admin/manager) sem autorização do chamador.
Impacto: Clientes anônimos podem se promover a admin.
Recomendação: Restringir alterações de papel a admins autenticados.

### [MÉDIO] Query N+1 na Listagem de Tasks
Arquivo: routes/task_routes.py:14-57
Descrição: GET /tasks carrega todas as tasks e depois User.query.get() e Category.query.get() por task.
Impacto: Performance degrada linearmente com a quantidade de tasks.
Recomendação: Usar joinedload ou query única com joins.

### [MÉDIO] Lógica de Overdue Duplicada
Arquivo: models/task.py:50-60 (não utilizado); routes/task_routes.py, user_routes.py, report_routes.py
Descrição: Mesma condicional de overdue copiada 5+ vezes; método do model ignorado.
Impacto: Comportamento inconsistente se a lógica mudar em um lugar.
Recomendação: Centralizar em Task.is_overdue().

### [MÉDIO] Configuração de Runtime Insegura para Produção
Arquivo: app.py:15,30-31,34
Descrição: CORS(app) permite todas as origens; debug=True; db.create_all() no import.
Impacto: Debug expõe stack traces; CORS aberto permite abuso.
Recomendação: Config baseada em ambiente; padrão app factory.

### [MÉDIO] Cláusulas except Nuas
Arquivo: routes/user_routes.py:130; routes/task_routes.py:62
Descrição: Múltiplos blocos except nus retornam 500 genéricos sem logging estruturado.
Impacto: Depuração difícil; bugs aparecem como falhas opacas.
Recomendação: Capturar exceções específicas; usar error handler global.

### [MÉDIO] Queries Agregadas Ineficientes nos Relatórios
Arquivo: routes/report_routes.py:24-68
Descrição: Summary executa 9+ queries COUNT separadas mais loops Python sobre todas as tasks/usuários.
Impacto: Escalabilidade ruim conforme os dados crescem.
Recomendação: Usar SQL GROUP BY e agregações condicionais.

### [BAIXO] Código Morto e Dependências Não Utilizadas
Arquivo: app.py:7; requirements.txt (marshmallow, requests, python-dotenv não usados)
Descrição: Helpers órfãos e notification service nunca importados.
Impacto: Codebase confuso; dependências inchadas.
Recomendação: Conectar ou remover módulos mortos.

================================
Total: 14 achados
================================

Fase 2 concluída. Prosseguir com a refatoração (Fase 3)? [s/n]
