"""
services/tenisfree_service.py
Camada de serviços — regras de negócio e acesso ao banco para Produto.
As rotas não devem conter lógica de persistência; toda interação com o
banco passa por aqui.
"""

from __future__ import annotations

from typing import Optional

from sqlalchemy.exc import IntegrityError, SQLAlchemyError

from app.extensions import db
from app.models.tenisfree import Produto


# ── Helpers internos ───────────────────────────────────────────────────────

def _commit() -> None:
    """Realiza commit e levanta RuntimeError em caso de falha."""
    try:
        db.session.commit()
    except SQLAlchemyError as exc:
        db.session.rollback()
        raise RuntimeError(f"Erro ao persistir dados: {exc}") from exc


# ── CRUD ───────────────────────────────────────────────────────────────────

def listar_produtos(
    busca: str = "",
    categoria: str = "",
    page: int = 1,
    per_page: int = 12,
):
    """Retorna paginação de produtos com filtros opcionais."""
    query = Produto.query

    if busca:
        termo = f"%{busca}%"
        query = query.filter(
            db.or_(
                Produto.nome.ilike(termo),
                Produto.marca.ilike(termo),
            )
        )

    if categoria:
        query = query.filter(Produto.categoria == categoria)

    return query.order_by(Produto.criado_em.desc()).paginate(
        page=page, per_page=per_page, error_out=False
    )


def obter_produto(produto_id: int) -> Optional[Produto]:
    """Retorna um produto pelo ID ou None se não existir."""
    return db.session.get(Produto, produto_id)


def obter_produto_ou_404(produto_id: int) -> Produto:
    """Retorna um produto ou aborta com 404."""
    from flask import abort

    produto = obter_produto(produto_id)
    if produto is None:
        abort(404, description=f"Produto #{produto_id} não encontrado.")
    return produto


def criar_produto(dados: dict) -> Produto:
    """Cria e persiste um novo Produto."""
    produto = Produto(**dados)
    db.session.add(produto)
    _commit()
    return produto


def atualizar_produto(produto_id: int, dados: dict) -> Produto:
    """Atualiza os campos de um Produto existente."""
    produto = obter_produto_ou_404(produto_id)

    for campo, valor in dados.items():
        setattr(produto, campo, valor)

    _commit()
    return produto


def excluir_produto(produto_id: int) -> None:
    """Remove um Produto do banco de dados."""
    produto = obter_produto_ou_404(produto_id)
    try:
        db.session.delete(produto)
        db.session.commit()
    except IntegrityError as exc:
        db.session.rollback()
        raise RuntimeError(
            "Não é possível excluir: o registro possui dependências."
        ) from exc
    except SQLAlchemyError as exc:
        db.session.rollback()
        raise RuntimeError(f"Erro ao excluir produto: {exc}") from exc


def listar_categorias() -> list[str]:
    """Retorna lista de categorias distintas cadastradas."""
    rows = db.session.query(Produto.categoria).distinct().order_by(Produto.categoria).all()
    return [r[0] for r in rows]
