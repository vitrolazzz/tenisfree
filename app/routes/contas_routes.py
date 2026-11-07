import hashlib
import secrets
from datetime import datetime, timedelta, timezone

from flask import Blueprint, flash, redirect, render_template, request, session, url_for

from app.extensions import db
from app.forms.contas_forms import (
    CriarContaForm,
    LoginForm,
    RecuperarSenhaForm,
    RedefinirSenhaForm,
)
from app.models.conta import Conta

contas_bp = Blueprint("contas", __name__)


@contas_bp.route("/criar", methods=["GET", "POST"])
def criar():
    form = CriarContaForm()
    if form.validate_on_submit():
        email = form.email.data.strip().lower()
        if Conta.query.filter_by(email=email).first():
            form.email.errors.append("Já existe uma conta com este e-mail.")
            return render_template("contas/criar_conta.html", form=form)

        conta = Conta(nome=form.nome.data.strip(), email=email)
        conta.definir_senha(form.senha.data)
        db.session.add(conta)
        db.session.commit()
        flash("Conta criada com sucesso! Você já pode entrar em TenisFree.", "success")
        return redirect(url_for("main.index"))

    return render_template("contas/criar_conta.html", form=form)


@contas_bp.route("/entrar", methods=["GET", "POST"])
def entrar():
    form = LoginForm()
    if form.validate_on_submit():
        conta = Conta.query.filter_by(email=form.email.data.strip().lower()).first()
        if conta is None or not conta.verificar_senha(form.senha.data):
            flash("E-mail ou senha incorretos.", "danger")
            return render_template("contas/entrar.html", form=form)

        session.clear()
        session["conta_id"] = conta.id
        session["conta_nome"] = conta.nome
        flash(f"Bem-vindo, {conta.nome}!", "success")
        return redirect(request.args.get("next") or url_for("main.index"))

    return render_template("contas/entrar.html", form=form)


@contas_bp.route("/sair", methods=["POST"])
def sair():
    session.clear()
    flash("Você saiu da sua conta.", "info")
    return redirect(url_for("main.index"))


@contas_bp.route("/esqueci-senha", methods=["GET", "POST"])
def esqueci_senha():
    form = RecuperarSenhaForm()
    if form.validate_on_submit():
        conta = Conta.query.filter_by(email=form.email.data.strip().lower()).first()
        if conta:
            token = secrets.token_urlsafe(32)
            conta.reset_token_hash = hashlib.sha256(token.encode()).hexdigest()
            conta.reset_token_expira_em = datetime.now(timezone.utc) + timedelta(minutes=30)
            db.session.commit()
            reset_url = url_for("contas.redefinir_senha", token=token, _external=True)
            flash(f"Link local de recuperação: {reset_url}", "info")
        else:
            flash("Se o e-mail estiver cadastrado, enviaremos um link de recuperação.", "info")
        return redirect(url_for("contas.esqueci_senha"))

    return render_template("contas/esqueci_senha.html", form=form)


@contas_bp.route("/redefinir-senha/<token>", methods=["GET", "POST"])
def redefinir_senha(token):
    token_hash = hashlib.sha256(token.encode()).hexdigest()
    conta = Conta.query.filter_by(reset_token_hash=token_hash).first()
    expiration = conta.reset_token_expira_em if conta else None
    if expiration and expiration.tzinfo is None:
        expiration = expiration.replace(tzinfo=timezone.utc)
    if conta is None or expiration is None or expiration < datetime.now(timezone.utc):
        flash("O link de recuperação é inválido ou expirou.", "danger")
        return redirect(url_for("contas.esqueci_senha"))

    form = RedefinirSenhaForm()
    if form.validate_on_submit():
        conta.definir_senha(form.senha.data)
        conta.reset_token_hash = None
        conta.reset_token_expira_em = None
        db.session.commit()
        flash("Senha redefinida com sucesso.", "success")
        return redirect(url_for("contas.entrar"))

    return render_template("contas/redefinir_senha.html", form=form)
