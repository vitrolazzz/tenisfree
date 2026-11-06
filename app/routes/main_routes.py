"""
routes/main_routes.py
Blueprint principal — página inicial e rotas gerais.
"""

from flask import Blueprint, render_template

from app.services import tenisfree_service as svc

main_bp = Blueprint("main", __name__)


@main_bp.route("/")
def index():
    """Página inicial / dashboard do marketplace."""
    destaques = svc.listar_produtos(per_page=6).items
    total = svc.listar_produtos(per_page=9999).total
    categorias = svc.listar_categorias()
    return render_template(
        "index.html",
        destaques=destaques,
        total=total,
        categorias=categorias,
    )
