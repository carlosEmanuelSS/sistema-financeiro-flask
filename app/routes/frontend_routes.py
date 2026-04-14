from flask import Blueprint, render_template

frontend_bp = Blueprint("frontend", __name__)


@frontend_bp.route("/")
def index():
    """Página inicial - Dashboard."""
    return render_template("index.html", active_page="home")


@frontend_bp.route("/users")
def users_page():
    """Página de gerenciamento de usuários."""
    return render_template("users.html", active_page="users")


@frontend_bp.route("/categories")
def categories_page():
    """Página de gerenciamento de categorias."""
    return render_template("categories.html", active_page="categories")


@frontend_bp.route("/transactions")
def transactions_page():
    """Página de gerenciamento de transações."""
    return render_template("transactions.html", active_page="transactions")


@frontend_bp.route("/history")
def history_page():
    """Página de histórico de auditoria."""
    return render_template("history.html", active_page="history")
