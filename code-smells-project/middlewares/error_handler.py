from flask import jsonify
import logging

logger = logging.getLogger(__name__)

def register_error_handlers(app):
    @app.errorhandler(404)
    def not_found(e):
        return jsonify({"erro": "Recurso não encontrado"}), 404

    @app.errorhandler(500)
    def internal_error(e):
        logger.exception("Erro interno: %s", e)
        return jsonify({"erro": "Erro interno do servidor"}), 500

    @app.errorhandler(Exception)
    def handle_exception(e):
        logger.exception("Exceção não tratada: %s", e)
        return jsonify({"erro": "Erro interno do servidor"}), 500
