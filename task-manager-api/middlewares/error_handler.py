import logging

from flask import jsonify

logger = logging.getLogger(__name__)


def register_error_handlers(app):
    @app.errorhandler(404)
    def not_found(e):
        return jsonify({'error': 'Recurso não encontrado'}), 404

    @app.errorhandler(ValueError)
    def value_error(e):
        return jsonify({'error': str(e)}), 400

    @app.errorhandler(Exception)
    def handle_exception(e):
        logger.exception('Erro: %s', e)
        return jsonify({'error': 'Erro interno do servidor'}), 500
