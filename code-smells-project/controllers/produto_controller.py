from flask import jsonify, request

from config.settings import CATEGORIAS_VALIDAS
from models import produto_model

def listar_produtos():
    produtos = produto_model.get_todos_produtos()
    return jsonify({"dados": produtos, "sucesso": True}), 200

def buscar_produto(produto_id):
    produto = produto_model.get_produto_por_id(produto_id)
    if not produto:
        return jsonify({"erro": "Produto não encontrado", "sucesso": False}), 404
    return jsonify({"dados": produto, "sucesso": True}), 200

def criar_produto():
    dados = request.get_json() or {}
    erro = _validar_produto(dados)
    if erro:
        return jsonify({"erro": erro}), 400
    produto_id = produto_model.criar_produto(
        dados["nome"], dados.get("descricao", ""), dados["preco"],
        dados["estoque"], dados.get("categoria", "geral"),
    )
    return jsonify({"dados": {"id": produto_id}, "sucesso": True, "mensagem": "Produto criado"}), 201

def atualizar_produto(produto_id):
    if not produto_model.get_produto_por_id(produto_id):
        return jsonify({"erro": "Produto não encontrado"}), 404
    dados = request.get_json() or {}
    erro = _validar_produto(dados)
    if erro:
        return jsonify({"erro": erro}), 400
    produto_model.atualizar_produto(
        produto_id, dados["nome"], dados.get("descricao", ""), dados["preco"],
        dados["estoque"], dados.get("categoria", "geral"),
    )
    return jsonify({"sucesso": True, "mensagem": "Produto atualizado"}), 200

def deletar_produto(produto_id):
    if not produto_model.get_produto_por_id(produto_id):
        return jsonify({"erro": "Produto não encontrado"}), 404
    produto_model.deletar_produto(produto_id)
    return jsonify({"sucesso": True, "mensagem": "Produto deletado"}), 200

def buscar_produtos():
    termo = request.args.get("q", "")
    categoria = request.args.get("categoria") or None
    preco_min = float(request.args.get("preco_min")) if request.args.get("preco_min") else None
    preco_max = float(request.args.get("preco_max")) if request.args.get("preco_max") else None
    resultados = produto_model.buscar_produtos(termo, categoria, preco_min, preco_max)
    return jsonify({"dados": resultados, "total": len(resultados), "sucesso": True}), 200

def _validar_produto(dados):
    if not dados:
        return "Dados inválidos"
    for campo in ("nome", "preco", "estoque"):
        if campo not in dados:
            return f"{campo.capitalize()} é obrigatório"
    if dados["preco"] < 0 or dados["estoque"] < 0:
        return "Preço e estoque não podem ser negativos"
    if len(dados["nome"]) < 2:
        return "Nome muito curto"
    categoria = dados.get("categoria", "geral")
    if categoria not in CATEGORIAS_VALIDAS:
        return f"Categoria inválida. Válidas: {CATEGORIAS_VALIDAS}"
    return None
