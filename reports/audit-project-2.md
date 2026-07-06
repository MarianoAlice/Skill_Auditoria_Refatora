================================
RELATÓRIO DE AUDITORIA DE ARQUITETURA
================================
Projeto: ecommerce-api-legacy
Stack:   JavaScript + Express
Arquivos: 3 analisados | ~182 linhas de código

## Resumo
CRÍTICO: 5 | ALTO: 4 | MÉDIO: 3 | BAIXO: 2

## Achados

### [CRÍTICO] Credenciais de Produção Hardcoded
Arquivo: src/utils.js:1-7
Descrição: Credenciais de banco de dados, chave live do gateway de pagamento e usuário SMTP hardcoded no código-fonte.
Impacto: Segredos expostos a qualquer pessoa com acesso ao repositório; viola boas práticas de gestão de segredos.
Recomendação: Mover todos os segredos para variáveis de ambiente.

### [CRÍTICO] God Class — AppManager
Arquivo: src/AppManager.js:4-141
Descrição: AppManager gerencia schema, seed, rotas, checkout, pagamentos, relatórios e exclusão de usuários em uma única classe.
Impacto: Impossível testar unitariamente em isolamento; viola completamente o SRP e o MVC.
Recomendação: Separar em models/, controllers/, routes/, services/.

### [CRÍTICO] Cartão de Crédito e Chave de Pagamento Logados
Arquivo: src/AppManager.js:45
Descrição: Checkout registra número completo do cartão e chave do gateway de pagamento no console.
Impacto: Violação PCI-DSS; PAN e segredos podem acabar em logs.
Recomendação: Nunca logar PAN ou segredos; mascarar dados do cartão.

### [CRÍTICO] Hash de Senha Quebrado (badCrypto)
Arquivo: src/utils.js:17-23; AppManager.js:68
Descrição: badCrypto() codifica senha em base64 em loop; senha seed em texto puro '123'.
Impacto: Senhas trivialmente adivinháveis; contas facilmente comprometidas.
Recomendação: Usar crypto.scrypt ou bcrypt com salt por usuário.

### [CRÍTICO] Endpoint Admin sem Autenticação
Arquivo: src/AppManager.js:80-129
Descrição: GET /api/admin/financial-report expõe receita e PII sem autenticação.
Impacto: Qualquer cliente anônimo pode acessar dados financeiros sensíveis.
Recomendação: Adicionar autenticação JWT/sessão e controle de acesso baseado em papéis.

### [ALTO] Lógica de Negócio nos Handlers de Rota
Arquivo: src/AppManager.js:28-78
Descrição: Todo o fluxo de checkout vive inline no callback da rota Express.
Impacto: Lógica não pode ser reutilizada ou testada sem HTTP.
Recomendação: Extrair CheckoutService e CheckoutController.

### [ALTO] Callback Hell (Pirâmide da Perdição)
Arquivo: src/AppManager.js:37-77,89-127
Descrição: Até 5-6 níveis de callbacks aninhados db.get/db.run.
Impacto: Difícil de ler, propenso a erros, difícil adicionar transações.
Recomendação: Usar async/await com wrapper de banco promisificado.

### [ALTO] Padrão N+1 no Relatório Financeiro
Arquivo: src/AppManager.js:89-127
Descrição: Queries separadas por curso, matrícula, usuário e pagamento em loops aninhados.
Impacto: Performance degrada linearmente com o volume de dados.
Recomendação: Substituir por JOINs em uma única query agregada.

### [ALTO] Estado Global Mutável
Arquivo: src/utils.js:9-10,25
Descrição: globalCache e totalRevenue em nível de módulo exportados como estado compartilhado mutável.
Impacto: Acoplamento oculto e efeitos colaterais não testáveis.
Recomendação: Substituir por serviço de cache injetável ou remover.

### [MÉDIO] Banco de Dados em Memória — Sem Persistência
Arquivo: src/AppManager.js:7
Descrição: sqlite3.Database(':memory:') — todos os dados perdidos ao reiniciar.
Impacto: Inadequado para produção; matrículas somem após deploy.
Recomendação: Usar caminho SQLite em arquivo a partir da config.

### [MÉDIO] Registros Órfãos na Exclusão de Usuário
Arquivo: src/AppManager.js:131-137
Descrição: DELETE FROM users não faz cascade em enrollments ou payments.
Impacto: Violações de integridade de dados; exclusão LGPD incompleta.
Recomendação: Limpeza transacional nas tabelas relacionadas.

### [MÉDIO] Ausência de Tratamento Centralizado de Erros
Arquivo: src/app.js:5-14; AppManager.js com res.status(500) espalhados
Descrição: Sem error handler global; strings de erro ad-hoc.
Impacto: Respostas de API inconsistentes; ausência de headers de segurança padrão.
Recomendação: Adicionar middlewares/errorHandler.js com erros JSON consistentes.

### [BAIXO] Nomes de Variáveis Crípticos
Arquivo: src/AppManager.js:29-33
Descrição: Campos da requisição usam nomes opacos: usr, eml, pwd, c_id, cc.
Impacto: Prejudica legibilidade e descoberta da API.
Recomendação: Usar nomes descritivos nos controllers preservando o contrato da API.

### [BAIXO] Magic Numbers no Loop badCrypto
Arquivo: src/utils.js:19-22
Descrição: 10000 iterações de loop e substring(0, 10) sem constantes nomeadas.
Impacto: Obscurece a intenção; indica design copiado e colado.
Recomendação: Remover badCrypto; usar bibliotecas de criptografia padrão.

================================
Total: 14 achados
================================

Fase 2 concluída. Prosseguir com a refatoração (Fase 3)? [s/n]
