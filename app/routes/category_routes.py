from flask import Blueprint, request, jsonify
from app.services import category_service

category_bp = Blueprint("categories", __name__)


@category_bp.route("", methods=["GET"])
def list_categories():
    """Lista todas as categorias. Aceita filtro por user_id via query string."""
    user_id = request.args.get("user_id", type=int)
    if user_id:
        categories = category_service.get_categories_by_user(user_id)
    else:
        categories = category_service.get_all_categories()
    return jsonify([c.to_dict() for c in categories]), 200


@category_bp.route("/<int:category_id>", methods=["GET"])
def get_category(category_id):
    """Retorna uma categoria pelo ID."""
    category = category_service.get_category_by_id(category_id)
    if not category:
        return jsonify({"erro": "Categoria não encontrada."}), 404
    return jsonify(category.to_dict()), 200


@category_bp.route("", methods=["POST"])
def create_category():
    """Cria uma nova categoria."""
    data = request.get_json()
    if not data:
        return jsonify({"erro": "Corpo da requisição deve ser JSON."}), 400

    category, error = category_service.create_category(data)
    if error:
        if "não encontrado" in error:
            return jsonify({"erro": error}), 404
        return jsonify({"erro": error}), 400
    return jsonify(category.to_dict()), 201


@category_bp.route("/<int:category_id>", methods=["PUT"])
def update_category(category_id):
    """Atualiza uma categoria existente."""
    data = request.get_json()
    if not data:
        return jsonify({"erro": "Corpo da requisição deve ser JSON."}), 400

    category, error = category_service.update_category(category_id, data)
    if error:
        if "não encontrada" in error:
            return jsonify({"erro": error}), 404
        return jsonify({"erro": error}), 400
    return jsonify(category.to_dict()), 200


@category_bp.route("/<int:category_id>", methods=["DELETE"])
def delete_category(category_id):
    """Exclui uma categoria."""
    success, error = category_service.delete_category(category_id)
    if not success:
        return jsonify({"erro": error}), 404
    return jsonify({"mensagem": "Categoria excluída com sucesso."}), 200
