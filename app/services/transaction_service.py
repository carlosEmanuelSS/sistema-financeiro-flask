from datetime import datetime

from app import db
from app.models import Category, Transaction, TransactionHistory, User
from app.services.shared import ResourceNotFoundError, ValidationError


class TransactionService:
    VALID_TYPES = {"entrada", "saida"}

    @staticmethod
    def create_transaction(data):
        payload = TransactionService._validate_payload(data)

        transaction = Transaction(
            valor=payload["valor"],
            tipo=payload["tipo"],
            data=payload["data"],
            user_id=payload["user"].id,
            category_id=payload["category"].id,
        )
        db.session.add(transaction)
        db.session.flush()

        TransactionService._register_history(transaction.id, "create")
        db.session.commit()
        return transaction

    @staticmethod
    def list_transactions():
        return Transaction.query.order_by(Transaction.data.desc(), Transaction.id.desc()).all()

    @staticmethod
    def get_transaction(transaction_id):
        transaction = Transaction.query.get(transaction_id)
        if not transaction:
            raise ResourceNotFoundError("Transacao nao encontrada.")
        return transaction

    @staticmethod
    def update_transaction(transaction_id, data):
        transaction = TransactionService.get_transaction(transaction_id)
        payload = TransactionService._validate_payload(
            data,
            current_transaction=transaction,
        )

        transaction.valor = payload["valor"]
        transaction.tipo = payload["tipo"]
        transaction.data = payload["data"]
        transaction.user_id = payload["user"].id
        transaction.category_id = payload["category"].id

        TransactionService._register_history(transaction.id, "update")
        db.session.commit()
        return transaction

    @staticmethod
    def delete_transaction(transaction_id):
        transaction = TransactionService.get_transaction(transaction_id)
        TransactionService._register_history(transaction.id, "delete")
        db.session.commit()
        db.session.delete(transaction)
        db.session.commit()

    @staticmethod
    def _validate_payload(data, current_transaction=None):
        valor = data.get("valor", current_transaction.valor if current_transaction else None)
        tipo = data.get("tipo", current_transaction.tipo if current_transaction else None)
        data_transacao = data.get("data", current_transaction.data.isoformat() if current_transaction else None)
        user_id = data.get("user_id", current_transaction.user_id if current_transaction else None)
        category_id = data.get("category_id", current_transaction.category_id if current_transaction else None)

        if None in (valor, tipo, data_transacao, user_id, category_id):
            raise ValidationError(
                "Os campos valor, tipo, data, user_id e category_id sao obrigatorios."
            )

        try:
            valor = float(valor)
        except (TypeError, ValueError) as exc:
            raise ValidationError("O campo valor deve ser numerico.") from exc

        if valor <= 0:
            raise ValidationError("O valor da transacao deve ser positivo.")

        if tipo not in TransactionService.VALID_TYPES:
            raise ValidationError("O campo tipo deve ser 'entrada' ou 'saida'.")

        try:
            data_transacao = datetime.fromisoformat(data_transacao)
        except (TypeError, ValueError) as exc:
            raise ValidationError("O campo data deve estar no formato ISO 8601.") from exc

        user = User.query.get(user_id)
        if not user:
            raise ResourceNotFoundError("Usuario nao encontrado.")

        category = Category.query.get(category_id)
        if not category:
            raise ResourceNotFoundError("Categoria nao encontrada.")

        if category.user_id != user.id:
            raise ValidationError("A categoria informada nao pertence ao usuario.")

        return {
            "valor": valor,
            "tipo": tipo,
            "data": data_transacao,
            "user": user,
            "category": category,
        }

    @staticmethod
    def _register_history(transaction_id, action):
        history = TransactionHistory(transaction_id=transaction_id, acao=action)
        db.session.add(history)
