from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config

db = SQLAlchemy()
migrate = Migrate()


def create_app():
    """Factory da aplicação Flask."""
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)

    # Importar models para que o Migrate os detecte
    from app import models  # noqa: F401

    # Registrar blueprints da API
    from app.routes.user_routes import user_bp
    from app.routes.category_routes import category_bp
    from app.routes.transaction_routes import transaction_bp

    app.register_blueprint(user_bp, url_prefix="/api/users")
    app.register_blueprint(category_bp, url_prefix="/api/categories")
    app.register_blueprint(transaction_bp, url_prefix="/api/transactions")

    # Registrar blueprint do frontend
    from app.routes.frontend_routes import frontend_bp

    app.register_blueprint(frontend_bp)

    return app
