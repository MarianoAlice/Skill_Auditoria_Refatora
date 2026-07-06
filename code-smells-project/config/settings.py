import os

SECRET_KEY = os.environ.get("SECRET_KEY", "dev-only-change-in-production")
DEBUG = os.environ.get("FLASK_DEBUG", "false").lower() == "true"
DATABASE_PATH = os.environ.get("DATABASE_PATH", "loja.db")
HOST = os.environ.get("HOST", "0.0.0.0")
PORT = int(os.environ.get("PORT", "5000"))

CATEGORIAS_VALIDAS = [
    "informatica", "moveis", "vestuario", "geral", "eletronicos", "livros"
]

DISCOUNT_TIER_HIGH = 10000
DISCOUNT_TIER_MID = 5000
DISCOUNT_TIER_LOW = 1000
DISCOUNT_RATE_HIGH = 0.1
DISCOUNT_RATE_MID = 0.05
DISCOUNT_RATE_LOW = 0.02
