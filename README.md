# 💰 Sistema Financeiro Simplificado

**Aplicação web fullstack para gerenciamento financeiro pessoal** — Backend em Flask (API REST) com frontend integrado via templates Jinja2, utilizando SQLAlchemy como ORM e SQLite como banco de dados.

---

## 📌 1. Visão Geral do Sistema

### O Problema

O gerenciamento de finanças pessoais exige registro organizado de entradas e saídas de dinheiro, categorizadas por tipo de gasto ou receita, com rastreabilidade completa das operações realizadas. Sem um sistema estruturado, o controle financeiro torna-se propenso a erros, inconsistências e perda de informações.

### A Solução

O **Sistema Financeiro Simplificado** é uma aplicação **fullstack** que integra uma API REST robusta com uma interface web interativa, permitindo:

- **Cadastro de usuários** com validação de unicidade de email
- **Criação de categorias personalizadas** vinculadas a cada usuário (ex: Alimentação, Transporte, Lazer)
- **Registro de transações financeiras** do tipo entrada (receita) ou saída (despesa), associadas obrigatoriamente a um usuário e uma categoria
- **Auditoria completa** de todas as operações sobre transações (criação, edição e exclusão), armazenada automaticamente em uma tabela de histórico
- **Interface visual completa** com dashboard, formulários interativos e feedback em tempo real — sem necessidade de ferramentas externas como Postman

### Objetivo Principal

Demonstrar a construção de uma aplicação web fullstack com **arquitetura em camadas**, aplicando boas práticas de engenharia de software: separação de responsabilidades, validação robusta de regras de negócio, integridade referencial, rastreabilidade de operações e integração coesa entre backend e frontend.

---

## 🏗️ 2. Arquitetura do Sistema

O sistema segue uma abordagem **monolítica fullstack**, onde o backend Flask é responsável tanto pela API REST quanto pela entrega das páginas HTML ao navegador. Essa escolha arquitetural mantém a simplicidade do projeto, eliminando a necessidade de um servidor separado para o frontend.

### Visão Geral da Arquitetura

```
┌────────────────────────────────────────────────────────────────────────────┐
│                         NAVEGADOR DO USUÁRIO                               │
│                                                                            │
│  ┌──────────────────────┐         ┌──────────────────────────────────┐     │
│  │  Página HTML/CSS     │         │  JavaScript (Fetch API)          │     │
│  │  (renderizada pelo   │────────▶│  Envia requisições assíncronas   │     │
│  │   Jinja2 / Flask)    │         │  para a API REST (/api/*)        │     │
│  └──────────────────────┘         └───────────────┬──────────────────┘     │
│                                                   │ HTTP (JSON)            │
└───────────────────────────────────────────────────┼────────────────────────┘
                                                    │
                                                    ▼
┌────────────────────────────────────────────────────────────────────────────┐
│                          SERVIDOR FLASK                                    │
│                                                                            │
│  ┌────────────────────────────┐    ┌────────────────────────────────┐      │
│  │  Frontend Routes           │    │  API Routes (REST)             │      │
│  │  (frontend_routes.py)      │    │  (/api/users, /api/categories, │      │
│  │  Serve páginas HTML via    │    │   /api/transactions, etc.)     │      │
│  │  render_template()         │    │  Retorna dados em JSON         │      │
│  └────────────────────────────┘    └──────────────┬─────────────────┘      │
│                                                   │                        │
│                                    ┌──────────────▼─────────────────┐      │
│                                    │  Services (Lógica de Negócio)  │      │
│                                    │  Validações, regras, CRUD      │      │
│                                    └──────────────┬─────────────────┘      │
│                                                   │                        │
│                                    ┌──────────────▼─────────────────┐      │
│                                    │  Models (SQLAlchemy ORM)       │      │
│                                    │  Definição de tabelas e        │      │
│                                    │  relacionamentos               │      │
│                                    └──────────────┬─────────────────┘      │
│                                                   │                        │
└───────────────────────────────────────────────────┼────────────────────────┘
                                                    │
                                                    ▼
                                          ┌──────────────────┐
                                          │   SQLite (.db)   │
                                          └──────────────────┘
```

### Separação entre Frontend e Backend

| Camada | Responsabilidade | Comunicação |
|--------|-----------------|-------------|
| **Frontend** (HTML + CSS + JS) | Exibe a interface, captura ações do usuário e atualiza a tela dinamicamente | Envia requisições HTTP (Fetch API) para os endpoints `/api/*` |
| **Backend** (Flask + SQLAlchemy) | Processa requisições, aplica regras de negócio e persiste dados | Responde com JSON e status HTTP adequado (200, 201, 400, 404) |

A comunicação entre frontend e backend ocorre exclusivamente via **chamadas HTTP assíncronas** (AJAX), seguindo o padrão REST. O frontend nunca acessa o banco de dados diretamente — toda interação passa pela API.

---

## 🧱 3. Arquitetura de Camadas do Backend

O backend adota uma **arquitetura em três camadas** (Layered Architecture), onde cada camada possui uma responsabilidade única e bem definida. Essa separação garante que o código seja organizado, testável e de fácil manutenção.

### Diagrama da Arquitetura

```
Cliente (Browser / Postman)
        │
        ▼
┌─────────────────────────┐
│       ROUTES            │  ← Camada de Apresentação
│  (Recebe HTTP Request)  │     Recebe a requisição, extrai dados,
│  (Retorna HTTP Response)│     retorna resposta JSON com status HTTP
└────────────┬────────────┘
             │ Delega para
             ▼
┌─────────────────────────┐
│       SERVICES          │  ← Camada de Negócio
│  (Validações)           │     Executa TODAS as regras de negócio,
│  (Regras de Negócio)    │     validações e lógica da aplicação
│  (Operações no Banco)   │
└────────────┬────────────┘
             │ Utiliza
             ▼
┌─────────────────────────┐
│       MODELS            │  ← Camada de Dados
│  (Definição de tabelas) │     Define a estrutura do banco de dados
│  (Relacionamentos)      │     e os relacionamentos entre entidades
│  (Serialização)         │
└─────────────────────────┘
```

### Responsabilidade de Cada Camada

| Camada | Localização | Responsabilidade |
|--------|-------------|------------------|
| **Routes** | `app/routes/` | Receber requisições HTTP, extrair dados do corpo/query string, chamar o service correspondente e retornar a resposta JSON com o status HTTP adequado (200, 201, 400, 404). **Não contém regras de negócio.** |
| **Services** | `app/services/` | Concentrar **toda a lógica de negócio**: validação de campos obrigatórios, verificação de unicidade, checagem de pertencimento de categoria ao usuário, persistência no banco e registro de auditoria. |
| **Models** | `app/models.py` | Definir a estrutura das tabelas do banco via ORM (SQLAlchemy), configurar relacionamentos entre entidades, definir constraints (unique, nullable, foreign keys) e fornecer método `to_dict()` para serialização JSON. |

### Por que regras de negócio NÃO ficam nas rotas?

As rotas (controllers) atuam exclusivamente como **ponto de entrada e saída** da aplicação. Manter regras de negócio nas rotas causa:

- **Acoplamento** entre lógica HTTP e lógica de domínio
- **Duplicação de código** quando a mesma regra precisa ser aplicada em diferentes endpoints
- **Dificuldade de teste** unitário, pois testar regras exigiria simular requisições HTTP

No projeto, as rotas apenas delegam para os services e interpretam o resultado:

```python
# Exemplo: rota de criação de transação (transaction_routes.py)
@transaction_bp.route("", methods=["POST"])
def create_transaction():
    data = request.get_json()                                      # Extrai dados
    transaction, error = transaction_service.create_transaction(data)  # Delega ao service
    if error:
        return jsonify({"erro": error}), 400                       # Retorna erro
    return jsonify(transaction.to_dict()), 201                     # Retorna sucesso
```

Toda a validação (valor positivo, tipo válido, categoria pertence ao usuário, etc.) acontece **exclusivamente** dentro de `transaction_service.create_transaction()`.

---

## 🖥️ 4. Frontend da Aplicação

### O que é o Frontend

O frontend é a **interface visual** do sistema, construída com tecnologias nativas da web (HTML5, CSS3 e JavaScript puro). Ele permite que o usuário interaja com todas as funcionalidades do sistema — criar usuários, gerenciar categorias, registrar transações e consultar histórico de auditoria — de forma intuitiva, sem necessidade de ferramentas externas como Postman ou cURL.

As páginas são servidas pelo próprio Flask utilizando o motor de templates **Jinja2**, o que significa que o servidor renderiza a estrutura HTML e a entrega ao navegador. A partir desse ponto, o **JavaScript assume a comunicação assíncrona** com a API REST, atualizando a interface dinamicamente sem recarregar a página.

### Tecnologias do Frontend

| Tecnologia | Finalidade |
|------------|------------|
| **HTML5** | Estrutura semântica das páginas (formulários, tabelas, navegação) |
| **CSS3** | Estilização completa com tema dark, variáveis CSS, design responsivo e animações |
| **JavaScript (ES6+)** | Lógica do frontend: requisições assíncronas (`Fetch API`), manipulação do DOM, validações no cliente |
| **Jinja2** | Motor de templates do Flask para renderização server-side e herança de templates (`base.html`) |
| **Google Fonts (Inter)** | Tipografia moderna e legível |

### Como o Frontend se Comunica com a API

O frontend utiliza a **Fetch API** nativa do JavaScript para realizar chamadas HTTP assíncronas à API REST do backend. Toda a comunicação segue o padrão:

1. O usuário interage com a interface (clica em um botão, submete um formulário)
2. O JavaScript intercepta o evento e monta a requisição HTTP
3. A requisição é enviada para o endpoint REST correspondente (`/api/*`)
4. O backend processa, valida e retorna uma resposta JSON
5. O JavaScript interpreta a resposta e atualiza a interface dinamicamente

```javascript
// Função genérica de comunicação com a API (script.js)
async function apiRequest(endpoint, method = 'GET', body = null) {
  const options = {
    method,
    headers: { 'Content-Type': 'application/json' }
  };
  if (body) {
    options.body = JSON.stringify(body);
  }

  const response = await fetch(`/api${endpoint}`, options);
  const data = await response.json();

  if (!response.ok) {
    throw new Error(data.erro || 'Erro na requisição.');
  }
  return data;
}
```

### Páginas da Interface

| Página | Rota | Descrição |
|--------|------|-----------|
| **Dashboard** | `/` | Resumo financeiro com contadores (usuários, categorias, transações) e saldo total |
| **Usuários** | `/users` | CRUD completo de usuários com formulário e tabela dinâmica |
| **Categorias** | `/categories` | CRUD de categorias com filtro por usuário e vinculação automática |
| **Transações** | `/transactions` | Registro de entradas/saídas com resumo financeiro (entradas, saídas, saldo) |
| **Histórico** | `/history` | Consulta do log de auditoria com filtro por ID de transação |

### Recursos da Interface

- 🌙 **Tema dark** com variáveis CSS para fácil customização
- 📱 **Design responsivo** adaptado para dispositivos móveis e desktop
- ⚡ **Atualização dinâmica** via DOM — sem recarregamento de página
- 🔔 **Mensagens de feedback** (sucesso/erro) com auto-dismiss
- ⚠️ **Modal de confirmação** customizado para operações destrutivas (exclusão)
- 🔍 **Filtros interativos** por usuário e por transação
- 💰 **Formatação monetária** automática no padrão brasileiro (R$)

---

## 🔄 5. Integração Backend + Frontend

### Fluxo de Comunicação

O frontend e o backend se conectam através de **chamadas HTTP RESTful**. O frontend nunca acessa o banco de dados — toda operação passa obrigatoriamente pela API, que aplica as regras de negócio antes de persistir ou retornar dados.

### Exemplo Prático: Criar uma Transação pelo Frontend

O diagrama abaixo ilustra o fluxo completo quando um usuário cria uma transação pela interface web:

```
  ┌──────────────────────────────────────────────────────────────────┐
  │  FRONTEND (Navegador)                                            │
  │                                                                  │
  │  1. Usuário preenche o formulário:                               │
  │     → Valor: R$ 150,50                                           │
  │     → Tipo: entrada                                              │
  │     → Usuário: João Silva                                        │
  │     → Categoria: Salário                                         │
  │                                                                  │
  │  2. JavaScript captura o submit do formulário                    │
  │     → Previne recarregamento (e.preventDefault())                │
  │     → Monta o objeto JSON com os dados                           │
  │                                                                  │
  │  3. Fetch API envia POST para /api/transactions                  │
  │     → Content-Type: application/json                             │
  │     → Body: {"valor":150.5,"tipo":"entrada","user_id":1,...}     │
  └────────────────────────────┬─────────────────────────────────────┘
                               │ HTTP POST (JSON)
                               ▼
  ┌──────────────────────────────────────────────────────────────────┐
  │  BACKEND (Flask)                                                 │
  │                                                                  │
  │  4. Rota recebe a requisição                                     │
  │     → transaction_routes.py extrai o JSON                        │
  │     → Delega para transaction_service.create_transaction(data)   │
  │                                                                  │
  │  5. Service valida regras de negócio                             │
  │     → Valor > 0? ✅                                              │
  │     → Tipo válido ("entrada")? ✅                                │
  │     → Usuário existe? ✅                                         │
  │     → Categoria pertence ao usuário? ✅                          │
  │                                                                  │
  │  6. Service persiste no banco                                    │
  │     → INSERT na tabela transactions                              │
  │     → INSERT na tabela transaction_history (auditoria)           │
  │     → db.session.commit()                                        │
  │                                                                  │
  │  7. Retorna JSON com status 201                                  │
  │     → {"id":1,"valor":150.5,"tipo":"entrada",...}                │
  └────────────────────────────┬─────────────────────────────────────┘
                               │ HTTP 201 (JSON)
                               ▼
  ┌──────────────────────────────────────────────────────────────────┐
  │  FRONTEND (Navegador)                                            │
  │                                                                  │
  │  8. JavaScript recebe a resposta                                 │
  │     → Exibe mensagem de sucesso: "Entrada de R$ 150,50 criada"  │
  │     → Limpa o formulário                                         │
  │     → Recarrega a tabela de transações (novo GET /api/...)       │
  │     → Atualiza o resumo financeiro (entradas, saídas, saldo)     │
  └──────────────────────────────────────────────────────────────────┘
```

### Endpoints Consumidos pelo Frontend

| Ação na Interface | Método HTTP | Endpoint da API |
|-------------------|-------------|-----------------|
| Carregar dashboard | `GET` | `/api/users`, `/api/categories`, `/api/transactions` |
| Criar usuário | `POST` | `/api/users` |
| Excluir usuário | `DELETE` | `/api/users/:id` |
| Criar categoria | `POST` | `/api/categories` |
| Filtrar categorias | `GET` | `/api/categories?user_id=:id` |
| Excluir categoria | `DELETE` | `/api/categories/:id` |
| Criar transação | `POST` | `/api/transactions` |
| Filtrar transações | `GET` | `/api/transactions?user_id=:id` |
| Excluir transação | `DELETE` | `/api/transactions/:id` |
| Consultar histórico | `GET` | `/api/transactions/historico` |
| Filtrar histórico | `GET` | `/api/transactions/historico?transaction_id=:id` |

---

## 🗄️ 6. Estrutura do Banco de Dados

### Tabelas

| Tabela | Descrição | Campos Principais |
|--------|-----------|-------------------|
| `users` | Cadastro de usuários do sistema | `id` (PK), `nome`, `email` (UNIQUE) |
| `categories` | Categorias de transações, pertencentes a um usuário | `id` (PK), `nome`, `user_id` (FK → users) |
| `transactions` | Transações financeiras (entradas e saídas) | `id` (PK), `valor`, `tipo`, `data`, `user_id` (FK → users), `category_id` (FK → categories) |
| `transaction_history` | Log de auditoria sobre operações em transações | `id` (PK), `transaction_id`, `acao`, `data` |

### Diagrama Entidade-Relacionamento

```
┌──────────────────┐         ┌──────────────────────┐
│      users       │         │  transaction_history  │
├──────────────────┤         ├──────────────────────┤
│ id (PK)          │──┐      │ id (PK)              │
│ nome (NOT NULL)  │  │      │ transaction_id (INT)  │
│ email (UNIQUE)   │  │      │ acao (VARCHAR)        │
└──────────────────┘  │      │ data (DATETIME)       │
        │             │      └──────────────────────┘
        │ 1:N         │
        ▼             │
┌──────────────────┐  │
│   categories     │  │
├──────────────────┤  │
│ id (PK)          │  │
│ nome (NOT NULL)  │  │
│ user_id (FK) ────┼──┘
└──────────────────┘
        │
        │ 1:N
        ▼
┌──────────────────┐
│  transactions    │
├──────────────────┤
│ id (PK)          │
│ valor (FLOAT)    │
│ tipo (VARCHAR)   │
│ data (DATETIME)  │
│ user_id (FK) ────┼──→ users.id
│ category_id (FK) ┼──→ categories.id
└──────────────────┘
```

### Relacionamentos e Integridade Referencial

| Relacionamento | Tipo | Comportamento de Exclusão |
|---------------|------|---------------------------|
| `User` → `Category` | 1 para N | **Cascade delete**: ao excluir um usuário, todas as suas categorias são removidas automaticamente |
| `User` → `Transaction` | 1 para N | **Cascade delete**: ao excluir um usuário, todas as suas transações são removidas automaticamente |
| `Category` → `Transaction` | 1 para N | **Cascade delete**: ao excluir uma categoria, todas as transações vinculadas são removidas automaticamente |

O comportamento de exclusão em cascata é configurado no ORM via `cascade="all, delete-orphan"`, garantindo que registros órfãos nunca permaneçam no banco de dados.

A tabela `transaction_history` **não possui Foreign Key** para `transactions`. Isso é intencional: o histórico deve ser **preservado mesmo após a exclusão** da transação original, permitindo auditoria retroativa.

---

## 🧠 7. Regras de Negócio

As regras de negócio estão **integralmente implementadas na camada de Services** (`app/services/`), nunca nas rotas. Cada regra é validada programaticamente antes de qualquer operação no banco de dados.

### 7.1 Validação de Valor Positivo

**Regra:** O campo `valor` de uma transação deve ser um número positivo (maior que zero).

**Implementação técnica:** O service tenta converter o valor recebido para `float`. Se a conversão falhar (`TypeError` ou `ValueError`), retorna erro. Se o valor for ≤ 0, a transação é rejeitada antes de qualquer interação com o banco.

```python
# transaction_service.py
try:
    valor = float(valor)
except (TypeError, ValueError):
    return None, "O campo 'valor' deve ser um número."

if valor <= 0:
    return None, "O campo 'valor' deve ser positivo (maior que zero)."
```

### 7.2 Restrição de Tipo de Transação

**Regra:** O campo `tipo` aceita exclusivamente dois valores: `"entrada"` (receita) ou `"saida"` (despesa).

**Implementação técnica:** Uma tupla constante `TIPOS_VALIDOS = ("entrada", "saida")` é definida no topo do módulo. O valor recebido é comparado contra essa tupla. Qualquer valor diferente é rejeitado com mensagem descritiva.

```python
TIPOS_VALIDOS = ("entrada", "saida")

if tipo not in TIPOS_VALIDOS:
    return None, f"O campo 'tipo' deve ser 'entrada' ou 'saida'. Recebido: '{tipo}'."
```

### 7.3 Validação de Categoria Pertencente ao Usuário

**Regra:** Uma transação só pode ser criada ou atualizada com uma categoria que pertença ao mesmo usuário da transação. Uma categoria do Usuário A não pode ser usada em transações do Usuário B.

**Implementação técnica:** O service realiza **duas consultas ao banco**: primeiro busca a categoria pelo `category_id`, depois compara o `user_id` da categoria encontrada com o `user_id` da transação. Se forem diferentes, a operação é rejeitada.

```python
# 1. Busca a categoria no banco
category = Category.query.get(category_id)
if not category:
    return None, "Categoria não encontrada."

# 2. Verifica se a categoria pertence ao usuário da transação
if category.user_id != user_id:
    return None, "A categoria informada não pertence ao usuário."
```

Esta validação é aplicada tanto na **criação** (`create_transaction`) quanto na **atualização** (`update_transaction`) de transações.

### 7.4 Unicidade de Email

**Regra:** Dois usuários não podem ter o mesmo email.

**Implementação técnica:** Antes de criar ou atualizar um usuário, o service consulta o banco pelo email informado. Se já existir um registro com aquele email (e não for o próprio usuário em caso de atualização), a operação é rejeitada.

```python
existing = get_user_by_email(email)
if existing and existing.id != user_id:
    return None, "Já existe um usuário com este email."
```

### 7.5 Registro Automático de Auditoria

**Regra:** Toda operação de criação, edição ou exclusão de transação gera automaticamente um registro na tabela `transaction_history`.

**Implementação técnica:** Uma função interna `_registrar_historico()` é chamada dentro de cada operação, utilizando `db.session.flush()` antes do registro de criação para garantir que o ID da transação já esteja disponível.

```python
def _registrar_historico(transaction_id, acao):
    historico = TransactionHistory(
        transaction_id=transaction_id,
        acao=acao,                          # "create", "update" ou "delete"
        data=datetime.now(timezone.utc),
    )
    db.session.add(historico)
```

| Operação | Momento do Registro | Ação Registrada |
|----------|---------------------|-----------------|
| Criação | Após `flush()`, antes do `commit()` | `"create"` |
| Atualização | Antes do `commit()` | `"update"` |
| Exclusão | Antes do `delete()` e `commit()` | `"delete"` |

---

## 🔁 8. Fluxo Completo de uma Transação

O diagrama a seguir descreve o fluxo completo de uma requisição `POST /api/transactions` desde a chegada até a resposta:

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    FLUXO: CRIAR TRANSAÇÃO                              │
│                    POST /api/transactions                              │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  1. REQUISIÇÃO CHEGA NA ROTA                                           │
│     → transaction_routes.py recebe o POST                              │
│     → Extrai o corpo JSON via request.get_json()                       │
│     → Se não for JSON válido, retorna 400 imediatamente                │
│                                                                         │
│  2. ROTA DELEGA PARA O SERVICE                                         │
│     → Chama transaction_service.create_transaction(data)               │
│     → Nenhuma validação é feita na rota                                │
│                                                                         │
│  3. SERVICE VALIDA CAMPOS OBRIGATÓRIOS                                 │
│     → Verifica presença de: valor, tipo, user_id, category_id          │
│     → Se algum campo estiver ausente, retorna erro com lista           │
│       dos campos faltantes                                             │
│                                                                         │
│  4. SERVICE VALIDA REGRAS DE NEGÓCIO                                   │
│     → Converte valor para float (rejeita se não for número)            │
│     → Verifica se valor > 0 (rejeita valores negativos ou zero)        │
│     → Verifica se tipo está em ("entrada", "saida")                    │
│                                                                         │
│  5. SERVICE CONSULTA O BANCO DE DADOS                                  │
│     → Busca User pelo user_id → se não existir, retorna erro          │
│     → Busca Category pelo category_id → se não existir, retorna erro  │
│     → Compara category.user_id com user_id da transação                │
│       → Se forem diferentes, retorna erro de pertencimento             │
│                                                                         │
│  6. SERVICE PERSISTE A TRANSAÇÃO                                       │
│     → Cria objeto Transaction com os dados validados                   │
│     → Adiciona ao session: db.session.add(transaction)                 │
│     → Executa db.session.flush() para gerar o ID                       │
│                                                                         │
│  7. SERVICE REGISTRA AUDITORIA                                         │
│     → Chama _registrar_historico(transaction.id, "create")             │
│     → Cria registro em transaction_history com ação "create"           │
│     → Executa db.session.commit() (persiste transação + histórico)     │
│                                                                         │
│  8. RESPOSTA É RETORNADA                                               │
│     → Service retorna (transaction, None) para a rota                  │
│     → Rota serializa via transaction.to_dict()                         │
│     → Retorna JSON com status HTTP 201 (Created)                       │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

### Fluxo em caso de ERRO

Se qualquer validação falhar nos passos 3, 4 ou 5:

1. O service retorna `(None, "mensagem de erro")`
2. A rota detecta o erro (`if error:`)
3. Retorna JSON `{"erro": "mensagem"}` com status HTTP 400 ou 404
4. **Nenhum dado é persistido no banco** — o rollback é implícito

---

## 🔗 9. Lista de Rotas da API

Base URL: `http://localhost:5000/api`

### 9.1 Usuários — `/api/users`

| Método | Rota | Descrição | Status Sucesso |
|--------|------|-----------|----------------|
| `GET` | `/api/users` | Lista todos os usuários | 200 |
| `GET` | `/api/users/:id` | Retorna um usuário pelo ID | 200 |
| `POST` | `/api/users` | Cria um novo usuário | 201 |
| `PUT` | `/api/users/:id` | Atualiza um usuário existente | 200 |
| `DELETE` | `/api/users/:id` | Exclui um usuário e todos os dados vinculados | 200 |

**Corpo do POST/PUT:**
```json
{
  "nome": "João Silva",
  "email": "joao@email.com"
}
```

**Exemplo de resposta (POST 201):**
```json
{
  "id": 1,
  "nome": "João Silva",
  "email": "joao@email.com"
}
```

---

### 9.2 Categorias — `/api/categories`

| Método | Rota | Descrição | Status Sucesso |
|--------|------|-----------|----------------|
| `GET` | `/api/categories` | Lista todas as categorias | 200 |
| `GET` | `/api/categories?user_id=1` | Filtra categorias por usuário | 200 |
| `GET` | `/api/categories/:id` | Retorna uma categoria pelo ID | 200 |
| `POST` | `/api/categories` | Cria uma nova categoria | 201 |
| `PUT` | `/api/categories/:id` | Atualiza uma categoria existente | 200 |
| `DELETE` | `/api/categories/:id` | Exclui uma categoria e suas transações | 200 |

**Corpo do POST:**
```json
{
  "nome": "Alimentação",
  "user_id": 1
}
```

---

### 9.3 Transações — `/api/transactions`

| Método | Rota | Descrição | Status Sucesso |
|--------|------|-----------|----------------|
| `GET` | `/api/transactions` | Lista todas as transações | 200 |
| `GET` | `/api/transactions?user_id=1` | Filtra transações por usuário | 200 |
| `GET` | `/api/transactions/:id` | Retorna uma transação pelo ID | 200 |
| `POST` | `/api/transactions` | Cria uma nova transação | 201 |
| `PUT` | `/api/transactions/:id` | Atualiza uma transação existente | 200 |
| `DELETE` | `/api/transactions/:id` | Exclui uma transação | 200 |

**Corpo do POST:**
```json
{
  "valor": 150.50,
  "tipo": "entrada",
  "user_id": 1,
  "category_id": 1,
  "data": "2025-01-15T10:30:00"
}
```

> O campo `data` é **opcional**. Se omitido, o sistema utiliza automaticamente a data e hora atual (UTC).

---

### 9.4 Histórico de Auditoria — `/api/transactions/historico`

| Método | Rota | Descrição | Status Sucesso |
|--------|------|-----------|----------------|
| `GET` | `/api/transactions/historico` | Lista todo o histórico de auditoria | 200 |
| `GET` | `/api/transactions/historico?transaction_id=1` | Filtra histórico por transação | 200 |

**Exemplo de resposta:**
```json
[
  {
    "id": 1,
    "transaction_id": 5,
    "acao": "create",
    "data": "2025-01-15T10:30:00.123456"
  },
  {
    "id": 2,
    "transaction_id": 5,
    "acao": "update",
    "data": "2025-01-15T11:00:00.654321"
  }
]
```

---

## ⚠️ 10. Tratamento de Erros

### Status HTTP Utilizados

| Código | Significado | Quando é Usado |
|--------|-------------|----------------|
| **200** | OK | Operação de leitura, atualização ou exclusão bem-sucedida |
| **201** | Created | Recurso criado com sucesso (POST) |
| **400** | Bad Request | Dados inválidos: campo ausente, valor negativo, tipo inválido, email duplicado, categoria não pertence ao usuário |
| **404** | Not Found | Recurso não encontrado: usuário, categoria ou transação inexistente |

### Padrão de Resposta de Erro

Todas as respostas de erro seguem o formato consistente:

```json
{
  "erro": "Mensagem descritiva do problema."
}
```

### Exemplos de Erros Tratados

| Situação | Status | Resposta |
|----------|--------|----------|
| Valor negativo | 400 | `{"erro": "O campo 'valor' deve ser positivo (maior que zero)."}` |
| Tipo inválido | 400 | `{"erro": "O campo 'tipo' deve ser 'entrada' ou 'saida'. Recebido: 'xyz'."}` |
| Categoria de outro usuário | 400 | `{"erro": "A categoria informada não pertence ao usuário."}` |
| Email duplicado | 400 | `{"erro": "Já existe um usuário com este email."}` |
| Usuário não encontrado | 404 | `{"erro": "Usuário não encontrado."}` |
| Campos ausentes | 400 | `{"erro": "Campos obrigatórios ausentes: valor, tipo."}` |
| Corpo não é JSON | 400 | `{"erro": "Corpo da requisição deve ser JSON."}` |

---

## 🧪 11. Como Executar o Projeto

### Pré-requisitos

- **Python 3.10** ou superior
- **pip** (gerenciador de pacotes Python)
- **Git** (opcional, para clonar o repositório)

### Passo a Passo

```bash
# 1. Clone o repositório
git clone <url-do-repositorio>
cd projeto-flesk

# 2. Crie o ambiente virtual
python -m venv venv

# 3. Ative o ambiente virtual
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# 4. Instale as dependências
pip install -r requirements.txt

# 5. Configure as variáveis de ambiente
# O arquivo .env já está incluído com valores padrão para desenvolvimento:
#   FLASK_APP=run.py
#   FLASK_ENV=development
#   DATABASE_URL=sqlite:///financeiro.db
#   SECRET_KEY=chave-secreta-dev-mude-em-producao

# 6. Inicialize o banco de dados com migrations
flask db init          # Apenas na primeira vez (já executado)
flask db migrate -m "criacao inicial"   # Apenas na primeira vez (já executado)
flask db upgrade       # Aplica as migrations no banco

# 7. Execute o servidor
flask run
```

### Acessando o Sistema

| Recurso | URL |
|---------|-----|
| **Interface Web (Frontend)** | `http://localhost:5000/` |
| **API REST (Backend)** | `http://localhost:5000/api/` |

> **Nota:** Como o frontend é servido pelo próprio Flask, **não é necessário rodar um servidor separado** para o frontend. Basta executar `flask run` e acessar `http://localhost:5000/` no navegador. Tanto a interface visual quanto a API REST ficam disponíveis na mesma porta.

---

## 📊 12. Tecnologias Utilizadas

| Tecnologia | Versão | Finalidade |
|------------|--------|------------|
| **Flask** | 3.1.1 | Microframework web para Python. Fornece o servidor HTTP, sistema de rotas (Blueprints), gerenciamento de requisições/respostas e renderização de templates. |
| **Flask-SQLAlchemy** | 3.1.1 | Integração do ORM SQLAlchemy com Flask. Permite definir modelos de dados como classes Python, mapeadas automaticamente para tabelas no banco de dados (Object-Relational Mapping). |
| **Flask-Migrate** | 4.1.0 | Extensão que integra o Alembic ao Flask para gerenciamento de migrations do banco de dados. Permite versionar alterações no schema sem perda de dados. |
| **python-dotenv** | 1.1.0 | Carregamento automático de variáveis de ambiente a partir do arquivo `.env`, permitindo configuração flexível sem hardcoding de credenciais no código-fonte. |
| **SQLite** | (built-in) | Banco de dados relacional embutido no Python. Escolhido pela praticidade: não requer instalação de servidor separado, ideal para desenvolvimento e prototipagem. |
| **HTML5 + CSS3 + JavaScript** | — | Frontend construído com tecnologias nativas da web, sem frameworks. Utiliza Fetch API para comunicação assíncrona com o backend, DOM manipulation para atualização dinâmica da interface e design responsivo com tema dark. |
| **Jinja2** | (incluso no Flask) | Motor de templates para renderização server-side das páginas HTML, com suporte a herança de templates e injeção dinâmica de variáveis. |

---

## 📁 13. Estrutura de Arquivos

```
projeto-flesk/
├── app/
│   ├── __init__.py                 # Factory da aplicação (create_app)
│   ├── models.py                   # Modelos: User, Category, Transaction, TransactionHistory
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── user_routes.py          # Endpoints REST — usuários
│   │   ├── category_routes.py      # Endpoints REST — categorias
│   │   ├── transaction_routes.py   # Endpoints REST — transações e histórico
│   │   └── frontend_routes.py      # Rotas que servem as páginas HTML
│   ├── services/
│   │   ├── __init__.py
│   │   ├── user_service.py         # Lógica de negócio — usuários
│   │   ├── category_service.py     # Lógica de negócio — categorias
│   │   └── transaction_service.py  # Lógica de negócio — transações e auditoria
│   ├── templates/                  # ── FRONTEND: Templates HTML ──
│   │   ├── base.html               # Template base (navegação + layout + imports)
│   │   ├── index.html              # Dashboard com resumo financeiro
│   │   ├── users.html              # Página de gerenciamento de usuários
│   │   ├── categories.html         # Página de gerenciamento de categorias
│   │   ├── transactions.html       # Página de gerenciamento de transações
│   │   └── history.html            # Página de histórico de auditoria
│   └── static/                     # ── FRONTEND: Arquivos estáticos ──
│       ├── style.css               # Estilos CSS (tema dark, variáveis, responsivo)
│       └── script.js               # JavaScript (Fetch API, DOM, modal de confirmação)
├── migrations/                     # Migrations do Flask-Migrate (Alembic)
├── instance/                       # Banco de dados SQLite (gerado automaticamente)
├── .env                            # Variáveis de ambiente
├── .gitignore                      # Arquivos ignorados pelo Git
├── config.py                       # Classe de configuração da aplicação
├── requirements.txt                # Dependências do projeto
├── run.py                          # Ponto de entrada da aplicação
└── README.md                       # Esta documentação
```

### Estrutura do Frontend (detalhe)

```
app/
├── templates/                      # Páginas HTML renderizadas pelo Jinja2
│   ├── base.html                   # Layout base com <nav>, imports CSS/JS
│   │                                 e blocos {% block %} para herança
│   ├── index.html                  # Herda base.html → Dashboard
│   ├── users.html                  # Herda base.html → CRUD de usuários
│   ├── categories.html             # Herda base.html → CRUD de categorias
│   ├── transactions.html           # Herda base.html → CRUD de transações
│   └── history.html                # Herda base.html → Log de auditoria
│
├── static/
│   ├── style.css                   # Design system completo:
│   │                                 → Variáveis CSS (cores, fontes, espaçamentos)
│   │                                 → Tema dark com contraste acessível
│   │                                 → Grid responsivo e componentes reutilizáveis
│   │                                 → Animações e transições suaves
│   │
│   └── script.js                   # Lógica do frontend:
│                                     → apiRequest() — wrapper do Fetch API
│                                     → Inicialização por página (data-page)
│                                     → CRUD completo via chamadas REST
│                                     → Modal de confirmação customizado
│                                     → Formatação de moeda (BRL) e datas
│
└── routes/
    └── frontend_routes.py          # Blueprint que serve cada página HTML
                                      via render_template() do Flask
```

---

## 🎯 14. Considerações Finais

O **Sistema Financeiro Simplificado** foi projetado e implementado como uma aplicação fullstack funcional, com foco nos seguintes princípios de engenharia de software:

### 🔒 Integridade de Dados
- Foreign Keys com exclusão em cascata impedem registros órfãos
- Constraints de unicidade no email garantem consistência
- Valores obrigatórios são validados antes de qualquer persistência
- O tipo de transação é restrito a um conjunto fechado de valores válidos

### 🧩 Separação de Responsabilidades
- **Routes** apenas recebem e respondem — zero lógica de negócio
- **Services** concentram toda a validação e regras do domínio
- **Models** definem exclusivamente a estrutura de dados
- Cada camada pode ser modificada independentemente sem afetar as demais

### 📜 Rastreabilidade e Auditoria
- Todo `create`, `update` e `delete` de transação gera registro automático
- O histórico é preservado mesmo após exclusão da transação original
- Timestamps UTC garantem consistência temporal independente de timezone

### ⚙️ Boas Práticas de Backend
- Padrão **Application Factory** (`create_app()`) para configuração modular
- Uso de **Blueprints** para organização de rotas em módulos independentes
- **ORM (SQLAlchemy)** eliminando SQL manual e prevenindo injeção de código
- **Migrations** versionadas (Flask-Migrate/Alembic) para evolução controlada do schema
- Respostas de erro padronizadas com mensagens descritivas em português
- Variáveis de ambiente via `.env` para separação de configuração e código

### 🖥️ Frontend Integrado
- Interface web completa servida pelo próprio Flask via Jinja2
- Comunicação assíncrona com a API REST via **Fetch API**
- Dashboard com resumo financeiro em tempo real
- Modal de confirmação customizado para operações destrutivas
- Design responsivo com tema dark adaptado para dispositivos móveis
- Manipulação dinâmica do DOM sem recarregamento de página

### 🏗️ Arquitetura e Design
- **Monolito bem estruturado**: backend e frontend coexistem de forma organizada
- **API REST desacoplada**: o frontend consome a mesma API que um cliente externo usaria
- **Herança de templates**: `base.html` centraliza layout, navegação e imports
- **Código JavaScript modular**: funções reutilizáveis, inicialização condicional por página

---

> **Nota:** Este sistema foi desenvolvido como projeto acadêmico com o objetivo de demonstrar domínio sobre desenvolvimento fullstack, arquitetura em camadas, regras de negócio, integridade referencial e boas práticas de engenharia de software com Python e Flask.
