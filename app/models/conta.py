from datetime import datetime, timezone

from werkzeug.security import check_password_hash, generate_password_hash

from app.extensions import db


class Conta(db.Model):
    __tablename__ = "contas"

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(180), nullable=False, unique=True, index=True)
    senha_hash = db.Column(db.String(255), nullable=False)
    criado_em = db.Column(
        db.DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )
    reset_token_hash = db.Column(db.String(64), nullable=True, index=True)
    reset_token_expira_em = db.Column(db.DateTime(timezone=True), nullable=True)

    def definir_senha(self, senha: str) -> None:
        self.senha_hash = generate_password_hash(senha, method="scrypt")

    def verificar_senha(self, senha: str) -> bool:
        return check_password_hash(self.senha_hash, senha)
