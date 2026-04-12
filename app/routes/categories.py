from flask import Blueprint, jsonify, request

from app.services.category_service import CategoryService
from app.services.shared import ResourceNotFoundError, ValidationError


categories_bp = Blueprint("categories", __name__)


@categories_bp.post("")
def create_category():
    try:
        category = CategoryService.create_category(request.get_json(silent=True) or {})
        return jsonify(category.to_dict()), 201
    except ValidationError as exc:
        return jsonify({"error": str(exc)}), 400
    except ResourceNotFoundError as exc:
        return jsonify({"error": str(exc)}), 404


@categories_bp.get("")
def list_categories():
    categories = CategoryService.list_categories()
    return jsonify([category.to_dict() for category in categories]), 200


@categories_bp.get("/<int:category_id>")
def get_category(category_id):
    try:
        category = CategoryService.get_category(category_id)
        return jsonify(category.to_dict()), 200
    except ResourceNotFoundError as exc:
        return jsonify({"error": str(exc)}), 404


@categories_bp.put("/<int:category_id>")
def update_category(category_id):
    try:
        category = CategoryService.update_category(category_id, request.get_json(silent=True) or {})
        return jsonify(category.to_dict()), 200
    except ValidationError as exc:
        return jsonify({"error": str(exc)}), 400
    except ResourceNotFoundError as exc:
        return jsonify({"error": str(exc)}), 404


@categories_bp.delete("/<int:category_id>")
def delete_category(category_id):
    try:
        CategoryService.delete_category(category_id)
        return jsonify({"message": "Categoria removida com sucesso."}), 200
    except ValidationError as exc:
        return jsonify({"error": str(exc)}), 400
    except ResourceNotFoundError as exc:
        return jsonify({"error": str(exc)}), 404
