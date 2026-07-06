from flask import Blueprint, request, jsonify
from datetime import datetime

from database import db
from models.task import Task
from models.user import User
from models.category import Category
from services import task_service

task_bp = Blueprint('tasks', __name__)


@task_bp.route('/tasks', methods=['GET'])
def get_tasks():
    return jsonify(task_service.list_tasks()), 200


@task_bp.route('/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    task = task_service.get_task(task_id)
    if not task:
        return jsonify({'error': 'Task não encontrada'}), 404
    return jsonify(task), 200


@task_bp.route('/tasks', methods=['POST'])
def create_task():
    data = request.get_json()
    if not data or not data.get('title'):
        return jsonify({'error': 'Título é obrigatório'}), 400
    if len(data['title']) < 3:
        return jsonify({'error': 'Título muito curto'}), 400
    if data.get('due_date'):
        try:
            data['due_date_parsed'] = datetime.strptime(data['due_date'], '%Y-%m-%d')
        except ValueError:
            return jsonify({'error': 'Formato de data inválido. Use YYYY-MM-DD'}), 400
    result = task_service.create_task(data)
    return jsonify(result), 201


@task_bp.route('/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    data = request.get_json() or {}
    result = task_service.update_task(task_id, data)
    if not result:
        return jsonify({'error': 'Task não encontrada'}), 404
    return jsonify(result), 200


@task_bp.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    if not task_service.delete_task(task_id):
        return jsonify({'error': 'Task não encontrada'}), 404
    return jsonify({'message': 'Task deletada com sucesso'}), 200


@task_bp.route('/tasks/search', methods=['GET'])
def search_tasks():
    query = request.args.get('q', '')
    status = request.args.get('status', '')
    priority = request.args.get('priority', '')
    user_id = request.args.get('user_id', '')
    tasks = Task.query
    if query:
        tasks = tasks.filter(db.or_(Task.title.like(f'%{query}%'), Task.description.like(f'%{query}%')))
    if status:
        tasks = tasks.filter(Task.status == status)
    if priority:
        tasks = tasks.filter(Task.priority == int(priority))
    if user_id:
        tasks = tasks.filter(Task.user_id == int(user_id))
    return jsonify([t.to_dict() for t in tasks.all()]), 200


@task_bp.route('/tasks/stats', methods=['GET'])
def task_stats():
    from sqlalchemy import func
    total = Task.query.count()
    status_counts = dict(db.session.query(Task.status, func.count(Task.id)).group_by(Task.status).all())
    overdue = sum(1 for t in Task.query.all() if t.is_overdue())
    done = status_counts.get('done', 0)
    return jsonify({
        'total': total,
        'pending': status_counts.get('pending', 0),
        'in_progress': status_counts.get('in_progress', 0),
        'done': done,
        'cancelled': status_counts.get('cancelled', 0),
        'overdue': overdue,
        'completion_rate': round((done / total) * 100, 2) if total > 0 else 0,
    }), 200
