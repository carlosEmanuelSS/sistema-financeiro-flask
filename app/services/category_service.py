from app import db
from app.models import Category, Transaction, User
from app.services.shared import ResourceNotFoundError, ValidationError


class CategoryService:
    @staticmethod
    def create_category(data):
        nome = (data.get("nome") or "").strip()
        user_id = data.get("user_id")

        if not nome or user_id is None:
            raise ValidationError("Os campos nome e user_id sao obrigatorios.")

        user = User.query.get(user_id)
        if not user:
            raise ResourceNotFoundError("Usuario nao encontrado para associar a categoria.")

        existing_category = Category.query.filter_by(nome=nome, user_id=user_id).first()
        if existing_category:
            raise ValidationError("Este usuario ja possui uma categoria com este nome.")

        category = Category(nome=nome, user_id=user_id)
        db.session.add(category)
        db.session.commit()
        return category

    @staticmethod
    def list_categories():
        return Category.query.order_by(Category.id.asc()).all()

    @staticmethod
    def get_category(category_id):
        category = Category.query.get(category_id)
        if not category:
            raise ResourceNotFoundError("Categoria nao encontrada.")
        return category

    @staticmethod
    def update_category(category_id, data):
        category = CategoryService.get_category(category_id)

        nome = data.get("nome")
        user_id = data.get("user_id")

        if nome is not None:
            nome = nome.strip()
            if not nome:
                raise ValidationError("O campo nome nao pode ser vazio.")
        else:
            nome = category.nome

        if user_id is None:
            user_id = category.user_id
        else:
            user = User.query.get(user_id)
            if not user:
                raise ResourceNotFoundError("Usuario nao encontrado para associar a categoria.")

        existing_category = Category.query.filter_by(nome=nome, user_id=user_id).first()
        if existing_category and existing_category.id != category.id:
            raise ValidationError("Este usuario ja possui uma categoria com este nome.")

        category.nome = nome
        category.user_id = user_id

        db.session.commit()
        return category

    @staticmethod
    def delete_category(category_id):
        category = CategoryService.get_category(category_id)
        has_transactions = Transaction.query.filter_by(category_id=category.id).first()
        if has_transactions:
            raise ValidationError(
                "Nao e possivel remover uma categoria que possui transacoes vinculadas."
            )
        db.session.delete(category)
        db.session.commit()
