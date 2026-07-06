import re

from database import db
from models.task import Task
from models.user import User


def list_users():
    users = User.query.all()
    return [{
        'id': u.id,
        'name': u.name,
        'email': u.email,
        'role': u.role,
        'active': u.active,
        'created_at': str(u.created_at),
        'task_count': len(u.tasks),
    } for u in users]


def get_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return None
    data = user.to_dict(include_tasks=True)
    return data


def create_user(data):
    name, email, password = data.get('name'), data.get('email'), data.get('password')
    role = data.get('role', 'user')
    if not name or not email or not password:
        raise ValueError('Nome, email e senha são obrigatórios')
    if not re.match(r'^[a-zA-Z0-9+_.-]+@[a-zA-Z0-9.-]+$', email):
        raise ValueError('Email inválido')
    if len(password) < 4:
        raise ValueError('Senha deve ter no mínimo 4 caracteres')
    if role not in ('user', 'admin', 'manager'):
        raise ValueError('Role inválido')
    if User.query.filter_by(email=email).first():
        raise ValueError('Email já cadastrado')
    user = User(name=name, email=email, role=role)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()
    return user.to_dict()


def login(email, password):
    user = User.query.filter_by(email=email).first()
    if not user or not user.check_password(password):
        return None, 'Credenciais inválidas'
    if not user.active:
        return None, 'Usuário inativo'
    return user, None


def get_user_tasks(user_id):
    user = User.query.get(user_id)
    if not user:
        return None
    tasks = Task.query.filter_by(user_id=user_id).all()
    return [t.to_dict() for t in tasks]
