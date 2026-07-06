import logging

from flask import jsonify

from database.connection import get_db

logger = logging.getLogger(__name__)

def health_check():
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT 1")
    counts = {}
    for tabela in ("produtos", "usuarios", "pedidos"):
        cursor.execute(f"SELECT COUNT(*) FROM {tabela}")
        counts[tabela] = cursor.fetchone()[0]
    return jsonify({
        "status": "ok",
        "database": "connected",
        "counts": counts,
        "versao": "1.0.0",
    }), 200

def index():
    return jsonify({
        "mensagem": "Bem-vindo à API da Loja",
        "versao": "1.0.0",
        "endpoints": {
            "produtos": "/produtos",
            "usuarios": "/usuarios",
            "pedidos": "/pedidos",
            "login": "/login",
            "relatorios": "/relatorios/vendas",
            "health": "/health",
        },
    })
