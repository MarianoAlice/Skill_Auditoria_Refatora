from werkzeug.security import check_password_hash, generate_password_hash

from database.connection import get_db

def _usuario_publico(row):
    return {
        "id": row["id"],
        "nome": row["nome"],
        "email": row["email"],
        "tipo": row["tipo"],
        "criado_em": row["criado_em"],
    }

def get_todos_usuarios():
    cursor = get_db().cursor()
    cursor.execute("SELECT id, nome, email, tipo, criado_em FROM usuarios")
    return [dict(r) for r in cursor.fetchall()]

def get_usuario_por_id(usuario_id):
    cursor = get_db().cursor()
    cursor.execute(
        "SELECT id, nome, email, tipo, criado_em FROM usuarios WHERE id = ?",
        (usuario_id,),
    )
    row = cursor.fetchone()
    return dict(row) if row else None

def criar_usuario(nome, email, senha, tipo="cliente"):
    db = get_db()
    cursor = db.cursor()
    cursor.execute(
        "INSERT INTO usuarios (nome, email, senha, tipo) VALUES (?, ?, ?, ?)",
        (nome, email, generate_password_hash(senha), tipo),
    )
    db.commit()
    return cursor.lastrowid

def login_usuario(email, senha):
    cursor = get_db().cursor()
    cursor.execute("SELECT * FROM usuarios WHERE email = ?", (email,))
    row = cursor.fetchone()
    if row and check_password_hash(row["senha"], senha):
        return _usuario_publico(row)
    return None
