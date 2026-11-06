# 👟 TenisFree

> Marketplace de tênis — CRUD completo com Flask, SQLAlchemy e identidade visual laranja/preto.

---

## 1. Descrição do Projeto

O **TenisFree** é um marketplace de tênis desenvolvido com Python e Flask.  
Permite cadastrar, consultar, editar e excluir produtos (tênis) por meio de uma interface responsiva, moderna e segura.

---

## 2. Tecnologias Utilizadas

| Camada | Tecnologia |
|---|---|
| Backend | Python 3.11+, Flask 3.x |
| ORM | Flask-SQLAlchemy / SQLAlchemy 2.x |
| Migrations | Flask-Migrate (Alembic) |
| Formulários / CSRF | Flask-WTF, WTForms |
| Banco de dados | SQLite (dev) · PostgreSQL / MySQL (prod) |
| Templates | Jinja2 |
| Frontend | HTML5, CSS3, JavaScript (Bootstrap 5) |
| Configuração | python-dotenv |
| Testes | pytest |

---

## 3. Estrutura de Diretórios

```
tenisfree/
│
├── app/
│   ├── __init__.py              # Application Factory
│   ├── extensions.py            # db, migrate, csrf
│   ├── config.py                # Configurações por ambiente
│   │
│   ├── models/
│   │   ├── __init__.py
│   │   └── tenisfree.py         # Model Produto
│   │
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── main_routes.py       # Blueprint principal (index)
│   │   └── tenisfree_routes.py  # Blueprint CRUD /produtos
│   │
│   ├── services/
│   │   ├── __init__.py
│   │   └── tenisfree_service.py # Regras de negócio e acesso ao banco
│   │
│   ├── forms/
│   │   ├── __init__.py
│   │   └── tenisfree_forms.py   # ProdutoForm (Flask-WTF)
│   │
│   ├── templates/
│   │   ├── base.html
│   │   ├── index.html
│   │   ├── errors/
│   │   │   ├── 404.html
│   │   │   └── 500.html
│   │   └── tenisfree/
│   │       ├── list.html
│   │       ├── detail.html
│   │       ├── create.html
│   │       └── edit.html
│   │
│   └── static/
│       ├── css/
│       │   ├── style.css        # Estilos globais
│       │   └── tenisfree.css    # Estilos específicos
│       ├── js/
│       │   ├── main.js          # Scripts globais
│       │   └── tenisfree.js     # Scripts da área de produtos
│       └── images/
│
├── migrations/                  # Histórico Alembic
├── tests/
│   ├── __init__.py
│   ├── conftest.py
│   └── test_tenisfree.py
│
├── .env.example
├── .gitignore
├── requirements.txt
├── run.py
└── README.md
```

---

## 4. Pré-requisitos

- Python 3.11 ou superior
- pip
- Git (opcional)

---

## 5. Criar e Ativar o Ambiente Virtual

**Windows (PowerShell):**
```powershell
python -m venv venv
venv\Scripts\Activate.ps1
```

**Linux / macOS:**
```bash
python3 -m venv venv
source venv/bin/activate
```

---

## 6. Instalar Dependências

```bash
pip install -r requirements.txt
```

---

## 7. Configurar Variáveis de Ambiente

```bash
# Windows
copy .env.example .env

# Linux / macOS
cp .env.example .env
```

Edite `.env` e ajuste:

| Variável | Descrição |
|---|---|
| `SECRET_KEY` | Chave secreta Flask — gere com `python -c "import secrets; print(secrets.token_hex(32))"` |
| `DATABASE_URL` | URI do banco (padrão: `sqlite:///tenisfree.db`) |
| `FLASK_ENV` | `development` ou `production` |
| `FLASK_PORT` | Porta (padrão: `5000`) |

---

## 8. Inicializar o Banco de Dados

```bash
# Inicializar repositório de migrations (apenas na primeira vez)
flask --app run:app db init

# Gerar a migration inicial
flask --app run:app db migrate -m "init"

# Aplicar ao banco
flask --app run:app db upgrade
```

> **Nota:** se preferir criar as tabelas diretamente sem migrations (apenas para desenvolvimento rápido):
> ```python
> # No terminal Python com o contexto da app
> from app import create_app
> from app.extensions import db
> app = create_app()
> with app.app_context():
>     db.create_all()
> ```

---

## 9. Executar Migrations Futuras

Sempre que alterar um Model:

```bash
flask --app run:app db migrate -m "descricao da alteracao"
flask --app run:app db upgrade
```

---

## 10. Iniciar a Aplicação

```bash
python run.py
```

Acesse em: **http://localhost:5000**

---

## 11. Executar os Testes

```bash
pytest tests/ -v
```

Para ver cobertura de código (requer `pytest-cov`):

```bash
pip install pytest-cov
pytest tests/ -v --cov=app --cov-report=term-missing
```

---

## Configurações Pendentes / Pontos de Atenção

> [!NOTE]
> Os itens abaixo precisam de definição pelo time de negócio antes de ir para produção:

- **Upload de imagem:** atualmente suporta URL externa. Para upload de arquivo local, implemente armazenamento (disco local, S3, GCS etc.) e adapte o model/form.
- **Autenticação:** não há sistema de login/usuários. Adicione Flask-Login se necessário.
- **Driver de banco para produção:** para PostgreSQL adicione `psycopg2-binary` ao `requirements.txt`; para MySQL, `PyMySQL`.
- **Regras de relacionamento:** se houver entidades como Usuário, Pedido etc., sinalize para expandir os models.
- **Deploy:** configure `FLASK_ENV=production` e um servidor WSGI (Gunicorn, uWSGI) + proxy reverso (Nginx).

---

## Licença

Este projeto é de uso interno/educacional. Ajuste a licença conforme necessário.
