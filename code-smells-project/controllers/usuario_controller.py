from flask import jsonify, request

from models import usuario_model

def listar_usuarios():
    return jsonify({"dados": usuario_model.get_todos_usuarios(), "sucesso": True}), 200

def buscar_usuario(usuario_id):
    usuario = usuario_model.get_usuario_por_id(usuario_id)
    if not usuario:
        return jsonify({"erro": "Usuário não encontrado"}), 404
    return jsonify({"dados": usuario, "sucesso": True}), 200

def criar_usuario():
    dados = request.get_json() or {}
    nome, email, senha = dados.get("nome"), dados.get("email"), dados.get("senha")
    if not nome or not email or not senha:
        return jsonify({"erro": "Nome, email e senha são obrigatórios"}), 400
    usuario_id = usuario_model.criar_usuario(nome, email, senha)
    return jsonify({"dados": {"id": usuario_id}, "sucesso": True}), 201

def login():
    dados = request.get_json() or {}
    email, senha = dados.get("email"), dados.get("senha")
    if not email or not senha:
        return jsonify({"erro": "Email e senha são obrigatórios"}), 400
    usuario = usuario_model.login_usuario(email, senha)
    if not usuario:
        return jsonify({"erro": "Email ou senha inválidos", "sucesso": False}), 401
    return jsonify({"dados": usuario, "sucesso": True, "mensagem": "Login OK"}), 200
