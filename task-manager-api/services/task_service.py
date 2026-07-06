from sqlalchemy.orm import joinedload

from database import db
from models.task import Task
from models.user import User
from models.category import Category
from services.notification_service import NotificationService

notification_service = NotificationService()


def list_tasks():
    tasks = Task.query.options(joinedload(Task.user), joinedload(Task.category)).all()
    return [t.to_dict(include_relations=True) for t in tasks]


def get_task(task_id):
    task = Task.query.options(joinedload(Task.user), joinedload(Task.category)).get(task_id)
    if not task:
        return None
    return task.to_dict(include_relations=True)


def create_task(data):
    task = Task()
    task.title = data['title']
    task.description = data.get('description', '')
    task.status = data.get('status', 'pending')
    task.priority = int(data.get('priority', 3))
    task.user_id = data.get('user_id')
    task.category_id = data.get('category_id')
    if data.get('due_date_parsed'):
        task.due_date = data['due_date_parsed']
    elif data.get('due_date'):
        from datetime import datetime
        task.due_date = datetime.strptime(data['due_date'], '%Y-%m-%d')
    if data.get('tags'):
        task.tags = ','.join(data['tags']) if isinstance(data['tags'], list) else data['tags']
    db.session.add(task)
    db.session.commit()
    if task.user_id:
        user = User.query.get(task.user_id)
        if user:
            notification_service.notify_task_assigned(user, task)
    return task.to_dict(include_relations=True)


def update_task(task_id, data):
    task = Task.query.get(task_id)
    if not task:
        return None
    for field in ('title', 'description', 'status', 'user_id', 'category_id'):
        if field in data:
            setattr(task, field, data[field])
    if 'priority' in data:
        task.priority = int(data['priority'])
    if 'tags' in data:
        task.tags = ','.join(data['tags']) if isinstance(data['tags'], list) else data['tags']
    db.session.commit()
    return task.to_dict(include_relations=True)


def delete_task(task_id):
    task = Task.query.get(task_id)
    if not task:
        return False
    db.session.delete(task)
    db.session.commit()
    return True
