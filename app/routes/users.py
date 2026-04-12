from flask import Blueprint, jsonify, request

from app.services.user_service import UserService, ResourceNotFoundError, ValidationError


users_bp = Blueprint("users", __name__)


@users_bp.post("")
def create_user():
    try:
        user = UserService.create_user(request.get_json(silent=True) or {})
        return jsonify(user.to_dict()), 201
    except ValidationError as exc:
        return jsonify({"error": str(exc)}), 400


@users_bp.get("")
def list_users():
    users = UserService.list_users()
    return jsonify([user.to_dict() for user in users]), 200


@users_bp.get("/<int:user_id>")
def get_user(user_id):
    try:
        user = UserService.get_user(user_id)
        return jsonify(user.to_dict()), 200
    except ResourceNotFoundError as exc:
        return jsonify({"error": str(exc)}), 404


@users_bp.put("/<int:user_id>")
def update_user(user_id):
    try:
        user = UserService.update_user(user_id, request.get_json(silent=True) or {})
        return jsonify(user.to_dict()), 200
    except ValidationError as exc:
        return jsonify({"error": str(exc)}), 400
    except ResourceNotFoundError as exc:
        return jsonify({"error": str(exc)}), 404


@users_bp.delete("/<int:user_id>")
def delete_user(user_id):
    try:
        UserService.delete_user(user_id)
        return jsonify({"message": "Usuario removido com sucesso."}), 200
    except ValidationError as exc:
        return jsonify({"error": str(exc)}), 400
    except ResourceNotFoundError as exc:
        return jsonify({"error": str(exc)}), 404
