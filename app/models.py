from datetime import datetime, timezone
from app import db


class User(db.Model):
    """Modelo de usuário."""

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    # Relacionamentos
    categories = db.relationship(
        "Category", backref="user", lazy=True, cascade="all, delete-orphan"
    )
    transactions = db.relationship(
        "Transaction", backref="user", lazy=True, cascade="all, delete-orphan"
    )

    def to_dict(self):
        return {
            "id": self.id,
            "nome": self.nome,
            "email": self.email,
        }


class Category(db.Model):
    """Modelo de categoria, pertencente a um usuário."""

    __tablename__ = "categories"

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(80), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    # Relacionamento
    transactions = db.relationship(
        "Transaction", backref="category", lazy=True, cascade="all, delete-orphan"
    )

    def to_dict(self):
        return {
            "id": self.id,
            "nome": self.nome,
            "user_id": self.user_id,
        }


class Transaction(db.Model):
    """Modelo de transação financeira."""

    __tablename__ = "transactions"

    id = db.Column(db.Integer, primary_key=True)
    valor = db.Column(db.Float, nullable=False)
    tipo = db.Column(db.String(10), nullable=False)  # "entrada" ou "saida"
    data = db.Column(
        db.DateTime, nullable=False, default=lambda: datetime.now(timezone.utc)
    )
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    category_id = db.Column(
        db.Integer, db.ForeignKey("categories.id"), nullable=False
    )

    def to_dict(self):
        return {
            "id": self.id,
            "valor": self.valor,
            "tipo": self.tipo,
            "data": self.data.isoformat(),
            "user_id": self.user_id,
            "category_id": self.category_id,
        }


class TransactionHistory(db.Model):
    """Histórico de ações sobre transações (auditoria)."""

    __tablename__ = "transaction_history"

    id = db.Column(db.Integer, primary_key=True)
    transaction_id = db.Column(db.Integer, nullable=False)
    acao = db.Column(db.String(10), nullable=False)  # create, update, delete
    data = db.Column(
        db.DateTime, nullable=False, default=lambda: datetime.now(timezone.utc)
    )

    def to_dict(self):
        return {
            "id": self.id,
            "transaction_id": self.transaction_id,
            "acao": self.acao,
            "data": self.data.isoformat(),
        }
