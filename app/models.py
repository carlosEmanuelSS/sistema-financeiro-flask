from datetime import datetime

from sqlalchemy import CheckConstraint

from app import db


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    categories = db.relationship(
        "Category",
        back_populates="user",
        cascade="all, delete-orphan",
        lazy=True,
    )
    transactions = db.relationship(
        "Transaction",
        back_populates="user",
        cascade="all, delete-orphan",
        lazy=True,
    )

    def to_dict(self):
        return {
            "id": self.id,
            "nome": self.nome,
            "email": self.email,
        }


class Category(db.Model):
    __tablename__ = "categories"
    __table_args__ = (
        db.UniqueConstraint("nome", "user_id", name="uq_category_nome_user"),
    )

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(120), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    user = db.relationship("User", back_populates="categories")
    transactions = db.relationship(
        "Transaction",
        back_populates="category",
        lazy=True,
    )

    def to_dict(self):
        return {
            "id": self.id,
            "nome": self.nome,
            "user_id": self.user_id,
        }


class Transaction(db.Model):
    __tablename__ = "transactions"
    __table_args__ = (
        CheckConstraint("valor > 0", name="ck_transaction_valor_positivo"),
        CheckConstraint("tipo IN ('entrada', 'saida')", name="ck_transaction_tipo_valido"),
    )

    id = db.Column(db.Integer, primary_key=True)
    valor = db.Column(db.Float, nullable=False)
    tipo = db.Column(db.String(20), nullable=False)
    data = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey("categories.id"), nullable=False)

    user = db.relationship("User", back_populates="transactions")
    category = db.relationship("Category", back_populates="transactions")

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
    __tablename__ = "transaction_history"

    id = db.Column(db.Integer, primary_key=True)
    transaction_id = db.Column(db.Integer, nullable=False)
    acao = db.Column(db.String(20), nullable=False)
    data = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "transaction_id": self.transaction_id,
            "acao": self.acao,
            "data": self.data.isoformat(),
        }
