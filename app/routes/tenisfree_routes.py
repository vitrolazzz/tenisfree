"""
routes/tenisfree_routes.py
Blueprint CRUD para a entidade Produto (tênis).
Prefixo: /produtos  (definido na Application Factory)
"""

from flask import (
    Blueprint,
    render_template,
    redirect,
    url_for,
    flash,
    request,
    abort,
)

from app.forms.tenisfree_forms import ProdutoForm
from app.services import tenisfree_service as svc

tenisfree_bp = Blueprint("tenisfree", __name__)


# ── Listar ────────────────────────────────────────────────────────────────

@tenisfree_bp.route("/")
def listar():
    busca = request.args.get("busca", "").strip()
    categoria = request.args.get("categoria", "").strip()
    page = request.args.get("page", 1, type=int)

    paginacao = svc.listar_produtos(busca=busca, categoria=categoria, page=page)
    categorias = svc.listar_categorias()

    return render_template(
        "tenisfree/list.html",
        paginacao=paginacao,
        busca=busca,
        categoria_filtro=categoria,
        categorias=categorias,
    )


# ── Detalhe ───────────────────────────────────────────────────────────────

@tenisfree_bp.route("/<int:produto_id>")
def detalhe(produto_id: int):
    produto = svc.obter_produto_ou_404(produto_id)
    return render_template("tenisfree/detail.html", produto=produto)


# ── Criar ─────────────────────────────────────────────────────────────────

@tenisfree_bp.route("/novo", methods=["GET", "POST"])
def criar():
    form = ProdutoForm()

    if form.validate_on_submit():
        dados = {
            "nome": form.nome.data.strip(),
            "marca": form.marca.data.strip(),
            "categoria": form.categoria.data,
            "tamanho": form.tamanho.data,
            "cor": form.cor.data.strip(),
            "preco": form.preco.data,
            "estoque": form.estoque.data,
            "descricao": form.descricao.data.strip() if form.descricao.data else None,
            "imagem_url": form.imagem_url.data.strip() if form.imagem_url.data else None,
        }

        try:
            produto = svc.criar_produto(dados)
            flash(f'Produto "{produto.nome}" cadastrado com sucesso!', "success")
            return redirect(url_for("tenisfree.detalhe", produto_id=produto.id))
        except RuntimeError as exc:
            flash(str(exc), "danger")

    return render_template("tenisfree/create.html", form=form)


# ── Editar ────────────────────────────────────────────────────────────────

@tenisfree_bp.route("/<int:produto_id>/editar", methods=["GET", "POST"])
def editar(produto_id: int):
    produto = svc.obter_produto_ou_404(produto_id)
    form = ProdutoForm(obj=produto)

    if form.validate_on_submit():
        dados = {
            "nome": form.nome.data.strip(),
            "marca": form.marca.data.strip(),
            "categoria": form.categoria.data,
            "tamanho": form.tamanho.data,
            "cor": form.cor.data.strip(),
            "preco": form.preco.data,
            "estoque": form.estoque.data,
            "descricao": form.descricao.data.strip() if form.descricao.data else None,
            "imagem_url": form.imagem_url.data.strip() if form.imagem_url.data else None,
        }

        try:
            svc.atualizar_produto(produto_id, dados)
            flash(f'Produto "{produto.nome}" atualizado com sucesso!', "success")
            return redirect(url_for("tenisfree.detalhe", produto_id=produto_id))
        except RuntimeError as exc:
            flash(str(exc), "danger")

    return render_template("tenisfree/edit.html", form=form, produto=produto)


# ── Excluir ───────────────────────────────────────────────────────────────

@tenisfree_bp.route("/<int:produto_id>/excluir", methods=["POST"])
def excluir(produto_id: int):
    """Exclusão via POST com token CSRF (formulário na página de detalhe)."""
    produto = svc.obter_produto_ou_404(produto_id)
    nome = produto.nome

    try:
        svc.excluir_produto(produto_id)
        flash(f'Produto "{nome}" excluído com sucesso.', "success")
    except RuntimeError as exc:
        flash(str(exc), "danger")
        return redirect(url_for("tenisfree.detalhe", produto_id=produto_id))

    return redirect(url_for("tenisfree.listar"))
