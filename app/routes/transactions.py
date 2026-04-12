from flask import Blueprint, jsonify, request

from app.services.shared import ResourceNotFoundError, ValidationError
from app.services.transaction_service import TransactionService


transactions_bp = Blueprint("transactions", __name__)


@transactions_bp.post("")
def create_transaction():
    try:
        transaction = TransactionService.create_transaction(request.get_json(silent=True) or {})
        return jsonify(transaction.to_dict()), 201
    except ValidationError as exc:
        return jsonify({"error": str(exc)}), 400
    except ResourceNotFoundError as exc:
        return jsonify({"error": str(exc)}), 404


@transactions_bp.get("")
def list_transactions():
    transactions = TransactionService.list_transactions()
    return jsonify([transaction.to_dict() for transaction in transactions]), 200


@transactions_bp.get("/<int:transaction_id>")
def get_transaction(transaction_id):
    try:
        transaction = TransactionService.get_transaction(transaction_id)
        return jsonify(transaction.to_dict()), 200
    except ResourceNotFoundError as exc:
        return jsonify({"error": str(exc)}), 404


@transactions_bp.put("/<int:transaction_id>")
def update_transaction(transaction_id):
    try:
        transaction = TransactionService.update_transaction(
            transaction_id, request.get_json(silent=True) or {}
        )
        return jsonify(transaction.to_dict()), 200
    except ValidationError as exc:
        return jsonify({"error": str(exc)}), 400
    except ResourceNotFoundError as exc:
        return jsonify({"error": str(exc)}), 404


@transactions_bp.delete("/<int:transaction_id>")
def delete_transaction(transaction_id):
    try:
        TransactionService.delete_transaction(transaction_id)
        return jsonify({"message": "Transacao removida com sucesso."}), 200
    except ResourceNotFoundError as exc:
        return jsonify({"error": str(exc)}), 404
