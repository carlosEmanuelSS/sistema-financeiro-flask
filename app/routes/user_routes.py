from flask import Blueprint, request, jsonify
from app.services import user_service

user_bp = Blueprint("users", __name__)


@user_bp.route("", methods=["GET"])
def list_users():
    """Lista todos os usuários."""
    users = user_service.get_all_users()
    return jsonify([u.to_dict() for u in users]), 200


@user_bp.route("/<int:user_id>", methods=["GET"])
def get_user(user_id):
    """Retorna um usuário pelo ID."""
    user = user_service.get_user_by_id(user_id)
    if not user:
        return jsonify({"erro": "Usuário não encontrado."}), 404
    return jsonify(user.to_dict()), 200


@user_bp.route("", methods=["POST"])
def create_user():
    """Cria um novo usuário."""
    data = request.get_json()
    if not data:
        return jsonify({"erro": "Corpo da requisição deve ser JSON."}), 400

    user, error = user_service.create_user(data)
    if error:
        return jsonify({"erro": error}), 400
    return jsonify(user.to_dict()), 201


@user_bp.route("/<int:user_id>", methods=["PUT"])
def update_user(user_id):
    """Atualiza um usuário existente."""
    data = request.get_json()
    if not data:
        return jsonify({"erro": "Corpo da requisição deve ser JSON."}), 400

    user, error = user_service.update_user(user_id, data)
    if error:
        if "não encontrado" in error:
            return jsonify({"erro": error}), 404
        return jsonify({"erro": error}), 400
    return jsonify(user.to_dict()), 200


@user_bp.route("/<int:user_id>", methods=["DELETE"])
def delete_user(user_id):
    """Exclui um usuário."""
    success, error = user_service.delete_user(user_id)
    if not success:
        return jsonify({"erro": error}), 404
    return jsonify({"mensagem": "Usuário excluído com sucesso."}), 200
