from flask import Blueprint, jsonify

from models.user import User
from models.task import Task
from services import report_service

report_bp = Blueprint('reports', __name__)


@report_bp.route('/reports/summary', methods=['GET'])
def summary_report():
    return jsonify(report_service.summary_report()), 200


@report_bp.route('/reports/user/<int:user_id>', methods=['GET'])
def user_report(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({'error': 'Usuário não encontrado'}), 404
    tasks = Task.query.filter_by(user_id=user_id).all()
    done = sum(1 for t in tasks if t.status == 'done')
    overdue = sum(1 for t in tasks if t.is_overdue())
    high_priority = sum(1 for t in tasks if t.priority <= 2)
    total = len(tasks)
    return jsonify({
        'user': {'id': user.id, 'name': user.name, 'email': user.email},
        'statistics': {
            'total_tasks': total,
            'done': done,
            'pending': sum(1 for t in tasks if t.status == 'pending'),
            'in_progress': sum(1 for t in tasks if t.status == 'in_progress'),
            'cancelled': sum(1 for t in tasks if t.status == 'cancelled'),
            'overdue': overdue,
            'high_priority': high_priority,
            'completion_rate': round((done / total) * 100, 2) if total > 0 else 0,
        },
    }), 200
