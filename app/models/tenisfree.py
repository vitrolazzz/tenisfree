"""
models/tenisfree.py
Model SQLAlchemy da entidade Produto (tênis para venda no marketplace).

Campos inferidos para um marketplace de tênis. Caso algum campo não
corresponda ao modelo de negócio real, sinalize para ajuste.
"""

from datetime import datetime, timezone
from app.extensions import db


class Produto(db.Model):
    """Representa um tênis cadastrado no marketplace TenisFree."""

    __tablename__ = "produtos"

    # ── Chave primária ─────────────────────────────────────────────────────
    id = db.Column(db.Integer, primary_key=True)

    # ── Dados principais ───────────────────────────────────────────────────
    nome = db.Column(db.String(150), nullable=False)
    marca = db.Column(db.String(100), nullable=False)
    categoria = db.Column(db.String(80), nullable=False)   # Ex.: Corrida, Casual, Esportivo
    descricao = db.Column(db.Text, nullable=True)

    # ── Especificações ─────────────────────────────────────────────────────
    tamanho = db.Column(db.String(10), nullable=False)     # Ex.: 38, 39, 40 …
    cor = db.Column(db.String(60), nullable=False)

    # ── Comercial ─────────────────────────────────────────────────────────
    preco = db.Column(db.Numeric(10, 2), nullable=False)
    estoque = db.Column(db.Integer, nullable=False, default=0)

    # ── Mídia (URL de imagem externa — não há upload neste escopo) ─────────
    # PLACEHOLDER: se houver upload de arquivo, substitua por lógica de
    # armazenamento local/cloud e remova este campo de URL simples.
    imagem_url = db.Column(db.String(500), nullable=True)

    # ── Auditoria ─────────────────────────────────────────────────────────
    criado_em = db.Column(
        db.DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )
    atualizado_em = db.Column(
        db.DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    # ── Representação ─────────────────────────────────────────────────────
    def __repr__(self) -> str:
        return f"<Produto id={self.id} nome={self.nome!r}>"

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "nome": self.nome,
            "marca": self.marca,
            "categoria": self.categoria,
            "descricao": self.descricao,
            "tamanho": self.tamanho,
            "cor": self.cor,
            "preco": float(self.preco),
            "estoque": self.estoque,
            "imagem_url": self.imagem_url,
            "criado_em": self.criado_em.isoformat(),
            "atualizado_em": self.atualizado_em.isoformat(),
        }
