================================
RELATÓRIO DE AUDITORIA DE ARQUITETURA
================================
Projeto: code-smells-project
Stack:   Python + Flask
Arquivos: 4 analisados | ~580 linhas de código

## Resumo
CRÍTICO: 5 | ALTO: 4 | MÉDIO: 3 | BAIXO: 2

## Achados

### [CRÍTICO] SQL Injection por Concatenação de Strings
Arquivo: models.py:28,47-49,58-60,68,92,109-110,127-128,140,155,158-165,174,188,220,224,280,291-293
Descrição: Quase todas as queries SQL concatenam entrada controlada pelo usuário em vez de usar placeholders parametrizados.
Impacto: Atacantes podem injetar SQL para burlar autenticação, exfiltrar ou corromper dados.
Recomendação: Substituir todas as queries montadas por string por statements parametrizados (placeholders ?).

### [CRÍTICO] Execução Arbitrária de SQL sem Autenticação
Arquivo: app.py:59-78
Descrição: POST /admin/query aceita SQL arbitrário no corpo da requisição e o executa sem autenticação.
Impacto: Comprometimento total do banco — qualquer cliente pode ler, modificar ou apagar todos os dados.
Recomendação: Remover este endpoint completamente.

### [CRÍTICO] Armazenamento e Exposição de Senhas em Texto Puro
Arquivo: models.py:72-87,89-103; controllers.py:128-134; database.py:75-82
Descrição: Senhas armazenadas em texto puro; get_todos_usuarios() retorna o campo senha nas respostas da API.
Impacto: Roubo de credenciais se o banco ou a API forem comprometidos.
Recomendação: Fazer hash das senhas com werkzeug/bcrypt; nunca retornar campos de senha nas respostas.

### [CRÍTICO] Chave Secreta Hardcoded Exposta no Endpoint de Health
Arquivo: app.py:7-8; controllers.py:286-289
Descrição: SECRET_KEY hardcoded como 'minha-chave-super-secreta-123' e exposta na resposta de GET /health.
Impacto: Falsificação de sessão e exposição de configuração para qualquer requisitante.
Recomendação: Carregar segredos de variáveis de ambiente; endpoint de health retorna apenas status não sensível.

### [CRÍTICO] Reset de Banco de Dados sem Autenticação
Arquivo: app.py:47-57
Descrição: POST /admin/reset-db apaga todas as tabelas sem autenticação.
Impacto: Perda total de dados e negação de serviço por qualquer cliente anônimo.
Recomendação: Remover o endpoint ou protegê-lo com autenticação de admin e guards de ambiente.

### [ALTO] God Class — models.py Contém Toda a Lógica de Domínio
Arquivo: models.py:1-314
Descrição: Arquivo único contém SQL, regras de negócio, criação de pedidos e lógica de relatório de vendas para 4 domínios.
Impacto: Impossível testar em isolamento; qualquer mudança afeta toda a aplicação.
Recomendação: Separar em models por domínio (produto, usuario, pedido).

### [ALTO] Ausência de Autenticação e Autorização
Arquivo: app.py:11-30; controllers.py (todos os handlers)
Descrição: Sem JWT, sessão ou verificação de papéis em endpoints sensíveis como GET /usuarios, GET /pedidos, PUT /pedidos/status.
Impacto: Qualquer pessoa pode listar usuários com senhas, visualizar pedidos e alterar status de pedidos.
Recomendação: Implementar middleware de autenticação com controle de acesso baseado em papéis.

### [ALTO] Lógica de Negócio e Efeitos Colaterais nos Controllers
Arquivo: controllers.py:208-210,247-250
Descrição: Controllers contêm efeitos colaterais de notificação via print() em vez de uma camada de serviço.
Impacto: Viola o SRP; efeitos colaterais não podem ser mockados ou substituídos em testes.
Recomendação: Extrair lógica de notificação para services/pedido_service.py.

### [ALTO] Conexão Global Singleton com o Banco de Dados
Arquivo: database.py:4-11
Descrição: Única conexão global db_connection compartilhada entre todas as requisições com check_same_thread=False.
Impacto: Condições de corrida e problemas de lock do SQLite sob carga concorrente.
Recomendação: Usar o objeto g do Flask para conexões por requisição.

### [MÉDIO] Problema de Queries N+1 na Listagem de Pedidos
Arquivo: models.py:171-233
Descrição: Queries separadas para itens e nomes de produtos dentro de loops aninhados por pedido.
Impacto: Performance degrada linearmente com a quantidade de pedidos.
Recomendação: Usar JOINs para buscar pedidos com itens em uma única query.

### [MÉDIO] Modo Debug e CORS Permissivo
Arquivo: app.py:7-9,88
Descrição: DEBUG=True, CORS(app) sem restrição de origens, debug=True na resposta de health em produção.
Impacto: Debug expõe stack traces; CORS aberto permite abuso cross-origin.
Recomendação: Carregar configuração de variáveis de ambiente; separar settings de dev/prod.

### [MÉDIO] Tratamento Genérico de Exceções Expõe Erros Internos
Arquivo: controllers.py (em todo o arquivo)
Descrição: Exception genérica capturada e str(e) retornado aos clientes.
Impacto: Vaza erros SQL e caminhos internos para atacantes.
Recomendação: Registrar error handlers centralizados; retornar mensagens genéricas.

### [BAIXO] Magic Numbers na Lógica de Desconto do Relatório de Vendas
Arquivo: models.py:256-262
Descrição: Limites de desconto (1000, 5000, 10000) e taxas (0.02, 0.05, 0.1) hardcoded inline.
Impacto: Regras de negócio opacas e difíceis de alterar.
Recomendação: Extrair para constantes nomeadas em config/settings.py.

### [BAIXO] Logging Baseado em print()
Arquivo: controllers.py:8,11,57,106,161,179,208-210,247-250
Descrição: Aplicação usa print() para logging e notificações.
Impacto: Sem níveis de log, sem rotação, inadequado para observabilidade em produção.
Recomendação: Usar o módulo logging do Python com handlers configuráveis.

================================
Total: 14 achados
================================

Fase 2 concluída. Prosseguir com a refatoração (Fase 3)? [s/n]
