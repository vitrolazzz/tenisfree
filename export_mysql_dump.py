from datetime import datetime
from decimal import Decimal
from pathlib import Path

from app import create_app
from app.extensions import db
from app.models.tenisfree import Produto


def sql_string(value: object) -> str:
    if value is None:
        return "NULL"
    if isinstance(value, bool):
        return "1" if value else "0"
    if isinstance(value, (int, float, Decimal)):
        return str(value)
    if isinstance(value, datetime):
        return "'" + value.strftime("%Y-%m-%d %H:%M:%S") + "'"

    text = str(value).replace("\\", "\\\\").replace("'", "''")
    return "'" + text + "'"


app = create_app("development")
with app.app_context():
    produtos = Produto.query.order_by(Produto.id).all()

lines = [
    "-- TenisFree MySQL/MariaDB dump",
    "-- Generated from the project's SQLite database",
    "",
    "CREATE DATABASE IF NOT EXISTS `tenisfree`",
    "  CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;",
    "USE `tenisfree`;",
    "",
    "DROP TABLE IF EXISTS `produtos`;",
    """CREATE TABLE `produtos` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `nome` VARCHAR(150) NOT NULL,
  `marca` VARCHAR(100) NOT NULL,
  `categoria` VARCHAR(80) NOT NULL,
  `descricao` TEXT NULL,
  `tamanho` VARCHAR(10) NOT NULL,
  `cor` VARCHAR(60) NOT NULL,
  `preco` DECIMAL(10,2) NOT NULL,
  `estoque` INT NOT NULL DEFAULT 0,
  `imagem_url` VARCHAR(500) NULL,
  `criado_em` DATETIME NULL,
  `atualizado_em` DATETIME NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;""",
]

if produtos:
    values = []
    for produto in produtos:
        row = [
            produto.id,
            produto.nome,
            produto.marca,
            produto.categoria,
            produto.descricao,
            produto.tamanho,
            produto.cor,
            produto.preco,
            produto.estoque,
            produto.imagem_url,
            produto.criado_em,
            produto.atualizado_em,
        ]
        values.append("(" + ", ".join(sql_string(value) for value in row) + ")")

    lines.extend([
        "",
        "INSERT INTO `produtos` (",
        "  `id`, `nome`, `marca`, `categoria`, `descricao`, `tamanho`, `cor`,",
        "  `preco`, `estoque`, `imagem_url`, `criado_em`, `atualizado_em`",
        ") VALUES",
        ",\n".join(values) + ";",
    ])

Path("tenisfree_mysql.sql").write_text("\n".join(lines) + "\n", encoding="utf-8")
print(f"Dump criado: tenisfree_mysql.sql ({len(produtos)} produtos)")
