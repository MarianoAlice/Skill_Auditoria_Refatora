from flask import Blueprint, request, jsonify

from database import db
from models.user import User
from services import user_service

user_bp = Blueprint('users', __name__)


@user_bp.route('/users', methods=['GET'])
def get_users():
    return jsonify(user_service.list_users()), 200


@user_bp.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = user_service.get_user(user_id)
    if not user:
        return jsonify({'error': 'Usuário não encontrado'}), 404
    return jsonify(user), 200


@user_bp.route('/users', methods=['POST'])
def create_user():
    try:
        return jsonify(user_service.create_user(request.get_json() or {})), 201
    except ValueError as e:
        return jsonify({'error': str(e)}), 400


@user_bp.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({'error': 'Usuário não encontrado'}), 404
    data = request.get_json() or {}
    if 'name' in data:
        user.name = data['name']
    if 'email' in data:
        user.email = data['email']
    if 'password' in data:
        user.set_password(data['password'])
    if 'role' in data:
        user.role = data['role']
    if 'active' in data:
        user.active = data['active']
    db.session.commit()
    return jsonify(user.to_dict()), 200


@user_bp.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({'error': 'Usuário não encontrado'}), 404
    for t in user.tasks:
        db.session.delete(t)
    db.session.delete(user)
    db.session.commit()
    return jsonify({'message': 'Usuário deletado com sucesso'}), 200


@user_bp.route('/users/<int:user_id>/tasks', methods=['GET'])
def get_user_tasks(user_id):
    tasks = user_service.get_user_tasks(user_id)
    if tasks is None:
        return jsonify({'error': 'Usuário não encontrado'}), 404
    return jsonify(tasks), 200


@user_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json() or {}
    email, password = data.get('email'), data.get('password')
    if not email or not password:
        return jsonify({'error': 'Email e senha são obrigatórios'}), 400
    user, err = user_service.login(email, password)
    if err:
        code = 403 if err == 'Usuário inativo' else 401
        return jsonify({'error': err}), code
    return jsonify({
        'message': 'Login realizado com sucesso',
        'user': user.to_dict(),
        'token': f'dev-token-{user.id}',
    }), 200
