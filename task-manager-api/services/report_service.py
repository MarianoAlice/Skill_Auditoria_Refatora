from datetime import datetime, timedelta

from database import db
from models.category import Category
from models.task import Task
from models.user import User
from sqlalchemy import func


def summary_report():
    total_tasks = Task.query.count()
    total_users = User.query.count()
    total_categories = Category.query.count()

    status_counts = dict(
        db.session.query(Task.status, func.count(Task.id)).group_by(Task.status).all()
    )
    priority_counts = dict(
        db.session.query(Task.priority, func.count(Task.id)).group_by(Task.priority).all()
    )

    all_tasks = Task.query.all()
    overdue_list = [
        {
            'id': t.id,
            'title': t.title,
            'due_date': str(t.due_date),
            'days_overdue': (datetime.utcnow() - t.due_date).days,
        }
        for t in all_tasks if t.is_overdue()
    ]

    seven_days_ago = datetime.utcnow() - timedelta(days=7)
    recent_tasks = Task.query.filter(Task.created_at >= seven_days_ago).count()
    recent_done = Task.query.filter(Task.status == 'done', Task.updated_at >= seven_days_ago).count()

    user_stats = []
    for u in User.query.all():
        total = len(u.tasks)
        completed = sum(1 for t in u.tasks if t.status == 'done')
        user_stats.append({
            'user_id': u.id,
            'user_name': u.name,
            'total_tasks': total,
            'completed_tasks': completed,
            'completion_rate': round((completed / total) * 100, 2) if total > 0 else 0,
        })

    return {
        'generated_at': str(datetime.utcnow()),
        'overview': {
            'total_tasks': total_tasks,
            'total_users': total_users,
            'total_categories': total_categories,
        },
        'tasks_by_status': {
            'pending': status_counts.get('pending', 0),
            'in_progress': status_counts.get('in_progress', 0),
            'done': status_counts.get('done', 0),
            'cancelled': status_counts.get('cancelled', 0),
        },
        'tasks_by_priority': {
            'critical': priority_counts.get(1, 0),
            'high': priority_counts.get(2, 0),
            'medium': priority_counts.get(3, 0),
            'low': priority_counts.get(4, 0),
            'minimal': priority_counts.get(5, 0),
        },
        'overdue': {'count': len(overdue_list), 'tasks': overdue_list},
        'recent_activity': {
            'tasks_created_last_7_days': recent_tasks,
            'tasks_completed_last_7_days': recent_done,
        },
        'user_productivity': user_stats,
    }


def list_categories():
    return [c.to_dict() for c in Category.query.all()]


def create_category(data):
    cat = Category(name=data['name'], description=data.get('description'), color=data.get('color', '#000000'))
    db.session.add(cat)
    db.session.commit()
    return cat.to_dict()
