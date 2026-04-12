from app.routes.categories import categories_bp
from app.routes.transactions import transactions_bp
from app.routes.users import users_bp


def register_blueprints(app):
    app.register_blueprint(users_bp, url_prefix="/users")
    app.register_blueprint(categories_bp, url_prefix="/categories")
    app.register_blueprint(transactions_bp, url_prefix="/transactions")
