# Sistema Financeiro Simplificado

API backend em Python com Flask para gerenciamento de usuarios, categorias e transacoes financeiras. O projeto foi organizado com separacao entre rotas, servicos e modelos, usando SQLite como banco de dados e Flask-Migrate para versionamento de schema.

## Tecnologias

- Flask
- Flask-SQLAlchemy
- Flask-Migrate
- python-dotenv
- SQLite

## ▶️ Execução Rápida

Copie e cole os comandos abaixo no terminal, na pasta do projeto:

```bash
# 1. Criar ambiente virtual
python -m venv venv

# 2. Ativar ambiente virtual
venv\Scripts\activate        # Windows
# source venv/bin/activate   # Linux/Mac

# 3. Instalar dependências
pip install -r requirements.txt

# 4. Criar o arquivo .env
copy .env.example .env       # Windows
# cp .env.example .env       # Linux/Mac

# 5. Criar o banco de dados via migrations
flask db upgrade

# 6. Rodar o projeto
flask run
```

> A API estará disponível em `http://127.0.0.1:5000`

## Estrutura do Projeto

```text
.
|-- app/
|   |-- __init__.py
|   |-- models.py
|   |-- routes/
|   |   |-- __init__.py
|   |   |-- users.py
|   |   |-- categories.py
|   |   `-- transactions.py
|   `-- services/
|       |-- __init__.py
|       |-- shared.py
|       |-- user_service.py
|       |-- category_service.py
|       `-- transaction_service.py
|-- migrations/
|   |-- README
|   |-- env.py
|   |-- script.py.mako
|   `-- versions/
|       `-- 0001_initial.py
|-- .env.example
|-- .flaskenv
|-- .gitignore
|-- config.py
|-- requirements.txt
|-- run.py
`-- README.md
```

## Banco de Dados e Migrations

> ⚠️ **O banco de dados NÃO é criado manualmente.** Ele é gerado automaticamente pelo **Flask-Migrate** (Alembic) ao rodar `flask db upgrade`. Esse comando aplica todas as migrations da pasta `migrations/versions/` e cria as tabelas no SQLite.

> Isso garante controle de versão do schema e reprodutibilidade — qualquer pessoa consegue recriar o banco idêntico com um único comando.

## 🧾 Script do Banco (CREATE TABLE)

> Os scripts abaixo representam a estrutura SQL gerada automaticamente pelo Flask-Migrate com base nos models definidos em `app/models.py`. **Não é necessário executar esses comandos manualmente** — o comando `flask db upgrade` cuida de tudo. Eles estão documentados aqui para fins de avaliação acadêmica.

```sql
-- Tabela de usuários
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome VARCHAR(120) NOT NULL,
    email VARCHAR(120) NOT NULL UNIQUE
);
```

```sql
-- Tabela de categorias (vinculada ao usuário)
CREATE TABLE categories (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome VARCHAR(120) NOT NULL,
    user_id INTEGER NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users (id),
    UNIQUE (nome, user_id)
);
```

```sql
-- Tabela de transações financeiras
CREATE TABLE transactions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    valor FLOAT NOT NULL,
    tipo VARCHAR(20) NOT NULL,
    data DATETIME NOT NULL DEFAULT (CURRENT_TIMESTAMP),
    user_id INTEGER NOT NULL,
    category_id INTEGER NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users (id),
    FOREIGN KEY (category_id) REFERENCES categories (id),
    CHECK (valor > 0),
    CHECK (tipo IN ('entrada', 'saida'))
);
```

```sql
-- Tabela de histórico de transações (auditoria)
CREATE TABLE transaction_history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    transaction_id INTEGER NOT NULL,
    acao VARCHAR(20) NOT NULL,
    data DATETIME NOT NULL DEFAULT (CURRENT_TIMESTAMP)
);
```

## Estrutura do Banco

### Tabela `users`

- `id`: chave primaria
- `nome`: nome do usuario
- `email`: email unico

### Tabela `categories`

- `id`: chave primaria
- `nome`: nome da categoria
- `user_id`: chave estrangeira para `users`

### Tabela `transactions`

- `id`: chave primaria
- `valor`: valor positivo da transacao
- `tipo`: `entrada` ou `saida`
- `data`: data/hora da transacao
- `user_id`: chave estrangeira para `users`
- `category_id`: chave estrangeira para `categories`

### Tabela `transaction_history`

- `id`: chave primaria
- `transaction_id`: identificador da transacao afetada
- `acao`: `create`, `update` ou `delete`
- `data`: data/hora do evento

## Relacionamentos

- User 1:N Categories
- User 1:N Transactions
- Category 1:N Transactions

## Regras de Negocio

- O valor da transacao deve ser sempre positivo
- O tipo da transacao deve ser apenas `entrada` ou `saida`
- Toda transacao deve possuir uma categoria valida
- A categoria informada deve pertencer ao mesmo usuario da transacao
- Toda criacao, edicao e exclusao de transacao gera um registro em `transaction_history`
- Nao e permitido remover usuario ou categoria quando houver transacoes vinculadas

## Rotas da API

### Users

- `POST /users`
- `GET /users`
- `GET /users/<id>`
- `PUT /users/<id>`
- `DELETE /users/<id>`

Exemplo de payload:

```json
{
  "nome": "Maria",
  "email": "maria@email.com"
}
```

### Categories

- `POST /categories`
- `GET /categories`
- `GET /categories/<id>`
- `PUT /categories/<id>`
- `DELETE /categories/<id>`

Exemplo de payload:

```json
{
  "nome": "Alimentacao",
  "user_id": 1
}
```

### Transactions

- `POST /transactions`
- `GET /transactions`
- `GET /transactions/<id>`
- `PUT /transactions/<id>`
- `DELETE /transactions/<id>`

Exemplo de payload:

```json
{
  "valor": 150.75,
  "tipo": "entrada",
  "data": "2026-04-11T10:30:00",
  "user_id": 1,
  "category_id": 1
}
```

## Respostas e Validacoes

- `400 Bad Request` para payload invalido ou violacao de regra de negocio
- `404 Not Found` para usuario, categoria ou transacao inexistente

## Como Executar

### Pré-requisitos

- Python 3.10 ou superior
- pip (gerenciador de pacotes do Python)
- Terminal/Prompt de comando

### Passo a passo

1. **Clone o repositório e entre na pasta:**

```bash
git clone <url-do-repositorio>
cd <nome-da-pasta>
```

2. **Crie e ative o ambiente virtual:**

```bash
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # Linux/Mac
```

3. **Instale as dependências:**

```bash
pip install -r requirements.txt
```

4. **Configure o arquivo `.env`:**

```bash
copy .env.example .env       # Windows
# cp .env.example .env       # Linux/Mac
```

O conteúdo do `.env` será:

```env
DATABASE_URL=sqlite:///financeiro.db
```

5. **Crie o banco de dados (via migrations):**

```bash
flask db upgrade
```

> O banco SQLite será criado automaticamente. Não é necessário criar tabelas manualmente.

6. **Inicie a aplicação:**

```bash
flask run
```

7. **Teste a API:**

Acesse `http://127.0.0.1:5000/` no navegador ou use Postman/Insomnia para testar as rotas.

## ✅ Atendimento aos Requisitos

| Requisito | Status | Detalhes |
|-----------|--------|----------|
| Backend em Flask | ✔️ | Framework principal da aplicação |
| Mínimo de 4 tabelas | ✔️ | `users`, `categories`, `transactions`, `transaction_history` |
| Relacionamento 1:N | ✔️ | User→Categories, User→Transactions, Category→Transactions |
| CRUD completo | ✔️ | Create, Read, Update, Delete em todas as entidades |
| Regras de negócio | ✔️ | Validações de valor, tipo, vínculo de categoria, histórico automático, proteção contra exclusão |
| Uso de `.env` | ✔️ | Variáveis de ambiente via `python-dotenv` (`.env` + `.flaskenv`) |
| Uso de `venv` | ✔️ | Ambiente virtual Python documentado e no `.gitignore` |
| Uso de migrations | ✔️ | Flask-Migrate/Alembic — banco criado via `flask db upgrade` |

## Observacoes

- O arquivo `.flaskenv` ja define `FLASK_APP=run.py`
- O endpoint `GET /` funciona como healthcheck simples
