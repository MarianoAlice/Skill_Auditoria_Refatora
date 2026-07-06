import logging

from flask import Flask
from flask_cors import CORS

from config import settings
from database.connection import init_db
from middlewares.error_handler import register_error_handlers
from views.routes import register_routes

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")

def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = settings.SECRET_KEY
    app.config["DEBUG"] = settings.DEBUG
    CORS(app)
    init_db(app)
    register_error_handlers(app)
    register_routes(app)
    return app

app = create_app()

if __name__ == "__main__":
    app.run(host=settings.HOST, port=settings.PORT, debug=settings.DEBUG)
