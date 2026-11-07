"""
app/__init__.py
Application Factory — cria e configura a instância Flask.
"""

import os
from flask import Flask, render_template

from app.extensions import db, migrate, csrf
from app.config import config_by_name


def create_app(config_name: str | None = None) -> Flask:
    """Cria e retorna a aplicação Flask configurada."""

    if config_name is None:
        config_name = os.environ.get("FLASK_ENV", "default")

    app = Flask(__name__)
    app.config.from_object(config_by_name[config_name])

    # ── Inicializar extensões ──────────────────────────────────────────────
    db.init_app(app)
    migrate.init_app(app, db)
    csrf.init_app(app)

    # ── Registrar Blueprints ───────────────────────────────────────────────
    from app.routes.main_routes import main_bp
    from app.routes.tenisfree_routes import tenisfree_bp
    from app.routes.contas_routes import contas_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(tenisfree_bp, url_prefix="/produtos")
    app.register_blueprint(contas_bp, url_prefix="/conta")

    # ── Páginas de erro ────────────────────────────────────────────────────
    @app.errorhandler(404)
    def page_not_found(e):
        return render_template("errors/404.html"), 404

    @app.errorhandler(500)
    def internal_error(e):
        db.session.rollback()
        return render_template("errors/500.html"), 500

    return app
