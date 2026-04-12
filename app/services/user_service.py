from app import db
from app.models import Transaction, User
from app.services.shared import ResourceNotFoundError, ValidationError


class UserService:
    @staticmethod
    def create_user(data):
        nome = (data.get("nome") or "").strip()
        email = (data.get("email") or "").strip().lower()

        if not nome or not email:
            raise ValidationError("Os campos nome e email sao obrigatorios.")

        if User.query.filter_by(email=email).first():
            raise ValidationError("Ja existe um usuario com este email.")

        user = User(nome=nome, email=email)
        db.session.add(user)
        db.session.commit()
        return user

    @staticmethod
    def list_users():
        return User.query.order_by(User.id.asc()).all()

    @staticmethod
    def get_user(user_id):
        user = User.query.get(user_id)
        if not user:
            raise ResourceNotFoundError("Usuario nao encontrado.")
        return user

    @staticmethod
    def update_user(user_id, data):
        user = UserService.get_user(user_id)

        nome = data.get("nome")
        email = data.get("email")

        if nome is not None:
            nome = nome.strip()
            if not nome:
                raise ValidationError("O campo nome nao pode ser vazio.")
            user.nome = nome

        if email is not None:
            email = email.strip().lower()
            if not email:
                raise ValidationError("O campo email nao pode ser vazio.")

            existing_user = User.query.filter_by(email=email).first()
            if existing_user and existing_user.id != user.id:
                raise ValidationError("Ja existe um usuario com este email.")

            user.email = email

        db.session.commit()
        return user

    @staticmethod
    def delete_user(user_id):
        user = UserService.get_user(user_id)
        has_transactions = Transaction.query.filter_by(user_id=user.id).first()
        if has_transactions:
            raise ValidationError(
                "Nao e possivel remover um usuario que possui transacoes vinculadas."
            )
        db.session.delete(user)
        db.session.commit()


ValidationError = ValidationError
ResourceNotFoundError = ResourceNotFoundError
