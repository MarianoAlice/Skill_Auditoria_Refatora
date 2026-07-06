from flask import Blueprint, request, jsonify

from database import db
from models.category import Category
from models.task import Task
from services import report_service

category_bp = Blueprint('categories', __name__)


@category_bp.route('/categories', methods=['GET'])
def get_categories():
    result = []
    for c in Category.query.all():
        cat_data = c.to_dict()
        cat_data['task_count'] = Task.query.filter_by(category_id=c.id).count()
        result.append(cat_data)
    return jsonify(result), 200


@category_bp.route('/categories', methods=['POST'])
def create_category():
    data = request.get_json() or {}
    if not data.get('name'):
        return jsonify({'error': 'Nome é obrigatório'}), 400
    return jsonify(report_service.create_category(data)), 201


@category_bp.route('/categories/<int:cat_id>', methods=['PUT'])
def update_category(cat_id):
    cat = Category.query.get(cat_id)
    if not cat:
        return jsonify({'error': 'Categoria não encontrada'}), 404
    data = request.get_json() or {}
    if 'name' in data:
        cat.name = data['name']
    if 'description' in data:
        cat.description = data['description']
    if 'color' in data:
        cat.color = data['color']
    db.session.commit()
    return jsonify(cat.to_dict()), 200


@category_bp.route('/categories/<int:cat_id>', methods=['DELETE'])
def delete_category(cat_id):
    cat = Category.query.get(cat_id)
    if not cat:
        return jsonify({'error': 'Categoria não encontrada'}), 404
    db.session.delete(cat)
    db.session.commit()
    return jsonify({'message': 'Categoria deletada'}), 200
