from flask import Blueprint, request, jsonify
from app.services import transaction_service
from app.models import TransactionHistory

transaction_bp = Blueprint("transactions", __name__)


@transaction_bp.route("", methods=["GET"])
def list_transactions():
    """Lista todas as transações. Aceita filtro por user_id via query string."""
    user_id = request.args.get("user_id", type=int)
    if user_id:
        transactions = transaction_service.get_transactions_by_user(user_id)
    else:
        transactions = transaction_service.get_all_transactions()
    return jsonify([t.to_dict() for t in transactions]), 200


@transaction_bp.route("/<int:transaction_id>", methods=["GET"])
def get_transaction(transaction_id):
    """Retorna uma transação pelo ID."""
    transaction = transaction_service.get_transaction_by_id(transaction_id)
    if not transaction:
        return jsonify({"erro": "Transação não encontrada."}), 404
    return jsonify(transaction.to_dict()), 200


@transaction_bp.route("", methods=["POST"])
def create_transaction():
    """Cria uma nova transação."""
    data = request.get_json()
    if not data:
        return jsonify({"erro": "Corpo da requisição deve ser JSON."}), 400

    transaction, error = transaction_service.create_transaction(data)
    if error:
        if "não encontrad" in error:
            return jsonify({"erro": error}), 404
        return jsonify({"erro": error}), 400
    return jsonify(transaction.to_dict()), 201


@transaction_bp.route("/<int:transaction_id>", methods=["PUT"])
def update_transaction(transaction_id):
    """Atualiza uma transação existente."""
    data = request.get_json()
    if not data:
        return jsonify({"erro": "Corpo da requisição deve ser JSON."}), 400

    transaction, error = transaction_service.update_transaction(transaction_id, data)
    if error:
        if "não encontrad" in error:
            return jsonify({"erro": error}), 404
        return jsonify({"erro": error}), 400
    return jsonify(transaction.to_dict()), 200


@transaction_bp.route("/<int:transaction_id>", methods=["DELETE"])
def delete_transaction(transaction_id):
    """Exclui uma transação."""
    success, error = transaction_service.delete_transaction(transaction_id)
    if not success:
        return jsonify({"erro": error}), 404
    return jsonify({"mensagem": "Transação excluída com sucesso."}), 200


@transaction_bp.route("/historico", methods=["GET"])
def list_history():
    """Lista todo o histórico de transações. Aceita filtro por transaction_id."""
    transaction_id = request.args.get("transaction_id", type=int)
    if transaction_id:
        history = TransactionHistory.query.filter_by(
            transaction_id=transaction_id
        ).all()
    else:
        history = TransactionHistory.query.all()
    return jsonify([h.to_dict() for h in history]), 200
