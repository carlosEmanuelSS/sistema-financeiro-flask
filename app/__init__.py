from flask import Flask, jsonify
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from config import Config


db = SQLAlchemy()
migrate = Migrate()


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)

    from app.routes import register_blueprints

    register_blueprints(app)

    @app.get("/")
    def healthcheck():
        return jsonify(
            {
                "message": "Sistema Financeiro Simplificado em execucao.",
                "status": "ok",
            }
        )

    return app
