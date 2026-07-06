from config import settings
from database.connection import get_db

def _pedidos_com_itens(rows):
    pedidos = {}
    for row in rows:
        pid = row["pedido_id"]
        if pid not in pedidos:
            pedidos[pid] = {
                "id": pid,
                "usuario_id": row["usuario_id"],
                "status": row["status"],
                "total": row["total"],
                "criado_em": row["criado_em"],
                "itens": [],
            }
        if row["produto_id"]:
            pedidos[pid]["itens"].append({
                "produto_id": row["produto_id"],
                "produto_nome": row["produto_nome"] or "Desconhecido",
                "quantidade": row["quantidade"],
                "preco_unitario": row["preco_unitario"],
            })
    return list(pedidos.values())

def _fetch_pedidos(where_clause="", params=()):
    query = f"""
        SELECT p.id AS pedido_id, p.usuario_id, p.status, p.total, p.criado_em,
               i.produto_id, i.quantidade, i.preco_unitario, pr.nome AS produto_nome
        FROM pedidos p
        LEFT JOIN itens_pedido i ON i.pedido_id = p.id
        LEFT JOIN produtos pr ON pr.id = i.produto_id
        {where_clause}
        ORDER BY p.id
    """
    cursor = get_db().cursor()
    cursor.execute(query, params)
    return _pedidos_com_itens(cursor.fetchall())

def get_pedidos_usuario(usuario_id):
    return _fetch_pedidos("WHERE p.usuario_id = ?", (usuario_id,))

def get_todos_pedidos():
    return _fetch_pedidos()

def criar_pedido(usuario_id, itens):
    db = get_db()
    cursor = db.cursor()
    total = 0
    produtos_cache = {}

    for item in itens:
        pid = item["produto_id"]
        cursor.execute("SELECT * FROM produtos WHERE id = ?", (pid,))
        produto = cursor.fetchone()
        if produto is None:
            return {"erro": f"Produto {pid} não encontrado"}
        if produto["estoque"] < item["quantidade"]:
            return {"erro": f"Estoque insuficiente para {produto['nome']}"}
        produtos_cache[pid] = produto
        total += produto["preco"] * item["quantidade"]

    try:
        cursor.execute(
            "INSERT INTO pedidos (usuario_id, status, total) VALUES (?, 'pendente', ?)",
            (usuario_id, total),
        )
        pedido_id = cursor.lastrowid
        for item in itens:
            produto = produtos_cache[item["produto_id"]]
            cursor.execute(
                "INSERT INTO itens_pedido (pedido_id, produto_id, quantidade, preco_unitario) VALUES (?, ?, ?, ?)",
                (pedido_id, item["produto_id"], item["quantidade"], produto["preco"]),
            )
            cursor.execute(
                "UPDATE produtos SET estoque = estoque - ? WHERE id = ?",
                (item["quantidade"], item["produto_id"]),
            )
        db.commit()
        return {"pedido_id": pedido_id, "total": total}
    except Exception:
        db.rollback()
        raise

def atualizar_status_pedido(pedido_id, novo_status):
    db = get_db()
    cursor = db.cursor()
    cursor.execute("UPDATE pedidos SET status = ? WHERE id = ?", (novo_status, pedido_id))
    db.commit()

def relatorio_vendas():
    cursor = get_db().cursor()
    cursor.execute("SELECT COUNT(*) FROM pedidos")
    total_pedidos = cursor.fetchone()[0]
    cursor.execute("SELECT SUM(total) FROM pedidos")
    faturamento = cursor.fetchone()[0] or 0
    cursor.execute("SELECT COUNT(*) FROM pedidos WHERE status = 'pendente'")
    pendentes = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM pedidos WHERE status = 'aprovado'")
    aprovados = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM pedidos WHERE status = 'cancelado'")
    cancelados = cursor.fetchone()[0]

    desconto = 0
    if faturamento > settings.DISCOUNT_TIER_HIGH:
        desconto = faturamento * settings.DISCOUNT_RATE_HIGH
    elif faturamento > settings.DISCOUNT_TIER_MID:
        desconto = faturamento * settings.DISCOUNT_RATE_MID
    elif faturamento > settings.DISCOUNT_TIER_LOW:
        desconto = faturamento * settings.DISCOUNT_RATE_LOW

    return {
        "total_pedidos": total_pedidos,
        "faturamento_bruto": round(faturamento, 2),
        "desconto_aplicavel": round(desconto, 2),
        "faturamento_liquido": round(faturamento - desconto, 2),
        "pedidos_pendentes": pendentes,
        "pedidos_aprovados": aprovados,
        "pedidos_cancelados": cancelados,
        "ticket_medio": round(faturamento / total_pedidos, 2) if total_pedidos > 0 else 0,
    }
