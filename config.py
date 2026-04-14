import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    """Configurações da aplicação carregadas do .env."""

    SECRET_KEY = os.getenv("SECRET_KEY", "chave-padrao-insegura")
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "sqlite:///financeiro.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
