"""
tests/test_tenisfree.py
Testes automatizados do CRUD de Produto.
"""

import pytest
from app.services import tenisfree_service as svc
from app.models.tenisfree import Produto


# ══════════════════════════════════════════════════════════════════════
# Testes de Serviço (camada de negócio)
# ══════════════════════════════════════════════════════════════════════

class TestCriarProduto:
    def test_cria_com_dados_validos(self, db, produto_base):
        produto = svc.criar_produto(produto_base)
        assert produto.id is not None
        assert produto.nome == "Air Test 90"
        assert float(produto.preco) == pytest.approx(299.90, rel=1e-2)

    def test_produto_persiste_no_banco(self, db, produto_base):
        produto = svc.criar_produto(produto_base)
        encontrado = svc.obter_produto(produto.id)
        assert encontrado is not None
        assert encontrado.nome == produto_base["nome"]


class TestListarProdutos:
    def test_lista_vazia_sem_erros(self, db):
        pag = svc.listar_produtos()
        assert pag is not None
        assert isinstance(pag.items, list)

    def test_lista_retorna_produto_cadastrado(self, db, produto_base):
        produto_base["nome"] = "Listar Test 01"
        svc.criar_produto(produto_base)
        pag = svc.listar_produtos(busca="Listar Test 01")
        nomes = [p.nome for p in pag.items]
        assert "Listar Test 01" in nomes

    def test_busca_por_marca(self, db, produto_base):
        produto_base["nome"] = "Busca Marca 01"
        produto_base["marca"] = "MarcaUnica"
        svc.criar_produto(produto_base)
        pag = svc.listar_produtos(busca="MarcaUnica")
        assert any(p.marca == "MarcaUnica" for p in pag.items)

    def test_filtro_por_categoria(self, db, produto_base):
        produto_base["nome"] = "Filtro Cat 01"
        produto_base["categoria"] = "Basquete"
        svc.criar_produto(produto_base)
        pag = svc.listar_produtos(categoria="Basquete")
        assert all(p.categoria == "Basquete" for p in pag.items)


class TestObterProduto:
    def test_obter_produto_existente(self, db, produto_base):
        produto = svc.criar_produto(produto_base)
        encontrado = svc.obter_produto(produto.id)
        assert encontrado is not None
        assert encontrado.id == produto.id

    def test_obter_produto_inexistente_retorna_none(self, db):
        assert svc.obter_produto(999999) is None


class TestAtualizarProduto:
    def test_atualiza_campos(self, db, produto_base, app):
        produto = svc.criar_produto(produto_base)
        with app.app_context():
            atualizado = svc.atualizar_produto(
                produto.id,
                {"nome": "Novo Nome", "preco": 399.00},
            )
            assert atualizado.nome == "Novo Nome"
            assert float(atualizado.preco) == pytest.approx(399.00, rel=1e-2)

    def test_atualiza_produto_inexistente_levanta_404(self, db, app):
        from flask import abort
        with app.app_context():
            with pytest.raises(Exception):  # werkzeug HTTPException (404)
                svc.atualizar_produto(999999, {"nome": "X"})


class TestExcluirProduto:
    def test_exclui_produto_existente(self, db, produto_base, app):
        produto = svc.criar_produto(produto_base)
        pid = produto.id
        with app.app_context():
            svc.excluir_produto(pid)
            assert svc.obter_produto(pid) is None

    def test_exclui_produto_inexistente_levanta_404(self, db, app):
        with app.app_context():
            with pytest.raises(Exception):
                svc.excluir_produto(999999)


# ══════════════════════════════════════════════════════════════════════
# Testes de Rota (camada HTTP)
# ══════════════════════════════════════════════════════════════════════

class TestRotas:
    def test_pagina_inicial_200(self, client):
        resp = client.get("/")
        assert resp.status_code == 200

    def test_listagem_200(self, client):
        resp = client.get("/produtos/")
        assert resp.status_code == 200

    def test_pagina_criar_get_200(self, client):
        resp = client.get("/produtos/novo")
        assert resp.status_code == 200

    def test_detalhe_produto_inexistente_404(self, client):
        resp = client.get("/produtos/999999")
        assert resp.status_code == 404

    def test_criar_produto_via_post(self, client, db, app):
        with app.app_context():
            with app.test_request_context():
                from flask_wtf.csrf import generate_csrf
                token = generate_csrf()

            resp = client.post(
                "/produtos/novo",
                data={
                    "csrf_token": token,
                    "nome": "HTTP Post Test",
                    "marca": "BrandHttp",
                    "categoria": "Casual",
                    "tamanho": "40",
                    "cor": "Branco",
                    "preco": "149.90",
                    "estoque": "5",
                    "descricao": "",
                    "imagem_url": "",
                },
                follow_redirects=True,
            )
            # CSRF desabilitado em testes (TestingConfig.WTF_CSRF_ENABLED = False)
            # então espera redirect bem-sucedido (200) ou 302
            assert resp.status_code in (200, 302)

    def test_listagem_busca_query_string(self, client):
        resp = client.get("/produtos/?busca=teste")
        assert resp.status_code == 200

    def test_rota_inexistente_404(self, client):
        resp = client.get("/rota-que-nao-existe")
        assert resp.status_code == 404
