from datetime import datetime, timezone
from app import db
from app.models import Transaction, TransactionHistory, User, Category


TIPOS_VALIDOS = ("entrada", "saida")


def _registrar_historico(transaction_id, acao):
    """Registra uma entrada no histórico de transações."""
    historico = TransactionHistory(
        transaction_id=transaction_id,
        acao=acao,
        data=datetime.now(timezone.utc),
    )
    db.session.add(historico)


def get_all_transactions():
    """Retorna todas as transações."""
    return Transaction.query.all()


def get_transaction_by_id(transaction_id):
    """Retorna uma transação pelo ID ou None."""
    return Transaction.query.get(transaction_id)


def get_transactions_by_user(user_id):
    """Retorna todas as transações de um usuário."""
    return Transaction.query.filter_by(user_id=user_id).all()


def create_transaction(data):
    """
    Cria uma nova transação com validações de negócio.
    Retorna (transaction, None) em sucesso ou (None, mensagem_erro) em falha.
    """
    valor = data.get("valor")
    tipo = data.get("tipo")
    user_id = data.get("user_id")
    category_id = data.get("category_id")
    data_str = data.get("data")

    # --- Validações obrigatórias ---
    campos_faltando = []
    if valor is None:
        campos_faltando.append("valor")
    if not tipo:
        campos_faltando.append("tipo")
    if user_id is None:
        campos_faltando.append("user_id")
    if category_id is None:
        campos_faltando.append("category_id")

    if campos_faltando:
        return None, f"Campos obrigatórios ausentes: {', '.join(campos_faltando)}."

    # Valor deve ser positivo
    try:
        valor = float(valor)
    except (TypeError, ValueError):
        return None, "O campo 'valor' deve ser um número."

    if valor <= 0:
        return None, "O campo 'valor' deve ser positivo (maior que zero)."

    # Tipo deve ser "entrada" ou "saida"
    if tipo not in TIPOS_VALIDOS:
        return None, f"O campo 'tipo' deve ser 'entrada' ou 'saida'. Recebido: '{tipo}'."

    # Usuário deve existir
    user = User.query.get(user_id)
    if not user:
        return None, "Usuário não encontrado."

    # Categoria deve existir
    category = Category.query.get(category_id)
    if not category:
        return None, "Categoria não encontrada."

    # Categoria deve pertencer ao usuário
    if category.user_id != user_id:
        return None, "A categoria informada não pertence ao usuário."

    # Data opcional
    if data_str:
        try:
            data_transacao = datetime.fromisoformat(data_str)
        except (TypeError, ValueError):
            return None, "O campo 'data' deve estar no formato ISO 8601 (ex: 2025-01-15T10:30:00)."
    else:
        data_transacao = datetime.now(timezone.utc)

    transaction = Transaction(
        valor=valor,
        tipo=tipo,
        data=data_transacao,
        user_id=user_id,
        category_id=category_id,
    )
    db.session.add(transaction)
    db.session.flush()  # Garante que o ID seja gerado antes de registrar histórico

    _registrar_historico(transaction.id, "create")
    db.session.commit()
    return transaction, None


def update_transaction(transaction_id, data):
    """
    Atualiza uma transação existente com validações de negócio.
    Retorna (transaction, None) em sucesso ou (None, mensagem_erro) em falha.
    """
    transaction = get_transaction_by_id(transaction_id)
    if not transaction:
        return None, "Transação não encontrada."

    # Valor
    if "valor" in data:
        try:
            valor = float(data["valor"])
        except (TypeError, ValueError):
            return None, "O campo 'valor' deve ser um número."
        if valor <= 0:
            return None, "O campo 'valor' deve ser positivo (maior que zero)."
        transaction.valor = valor

    # Tipo
    if "tipo" in data:
        if data["tipo"] not in TIPOS_VALIDOS:
            return None, f"O campo 'tipo' deve ser 'entrada' ou 'saida'. Recebido: '{data['tipo']}'."
        transaction.tipo = data["tipo"]

    # Categoria
    if "category_id" in data:
        category = Category.query.get(data["category_id"])
        if not category:
            return None, "Categoria não encontrada."
        if category.user_id != transaction.user_id:
            return None, "A categoria informada não pertence ao usuário."
        transaction.category_id = data["category_id"]

    # Data
    if "data" in data:
        try:
            transaction.data = datetime.fromisoformat(data["data"])
        except (TypeError, ValueError):
            return None, "O campo 'data' deve estar no formato ISO 8601."

    _registrar_historico(transaction.id, "update")
    db.session.commit()
    return transaction, None


def delete_transaction(transaction_id):
    """
    Exclui uma transação e registra no histórico.
    Retorna (True, None) em sucesso ou (False, mensagem_erro) em falha.
    """
    transaction = get_transaction_by_id(transaction_id)
    if not transaction:
        return False, "Transação não encontrada."

    _registrar_historico(transaction.id, "delete")
    db.session.delete(transaction)
    db.session.commit()
    return True, None
