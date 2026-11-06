"""
tests/conftest.py
Fixtures compartilhadas para os testes do TenisFree.
"""

import pytest
from app import create_app
from app.extensions import db as _db


@pytest.fixture(scope="session")
def app():
    """Cria a aplicação em modo de testes (SQLite em memória)."""
    application = create_app("testing")
    with application.app_context():
        _db.create_all()
        yield application
        _db.drop_all()


@pytest.fixture(scope="function")
def client(app):
    """Cliente HTTP de testes."""
    return app.test_client()


@pytest.fixture(scope="function")
def db(app):
    """Sessão de banco de dados — rollback após cada teste."""
    with app.app_context():
        yield _db
        _db.session.rollback()


@pytest.fixture
def produto_base() -> dict:
    """Dados válidos para criação de um Produto."""
    return {
        "nome": "Air Test 90",
        "marca": "TestBrand",
        "categoria": "Corrida",
        "tamanho": "42",
        "cor": "Preto",
        "preco": 299.90,
        "estoque": 10,
        "descricao": "Tênis para testes.",
        "imagem_url": None,
    }
