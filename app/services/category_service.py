from app import db
from app.models import Category, User


def get_all_categories():
    """Retorna todas as categorias."""
    return Category.query.all()


def get_category_by_id(category_id):
    """Retorna uma categoria pelo ID ou None."""
    return Category.query.get(category_id)


def get_categories_by_user(user_id):
    """Retorna todas as categorias de um usuário."""
    return Category.query.filter_by(user_id=user_id).all()


def create_category(data):
    """
    Cria uma nova categoria.
    Retorna (category, None) em sucesso ou (None, mensagem_erro) em falha.
    """
    nome = data.get("nome")
    user_id = data.get("user_id")

    if not nome or user_id is None:
        return None, "Os campos 'nome' e 'user_id' são obrigatórios."

    if isinstance(nome, str):
        nome = nome.strip()
    if not nome:
        return None, "O campo 'nome' não pode ser vazio."

    user = User.query.get(user_id)
    if not user:
        return None, "Usuário não encontrado."

    category = Category(nome=nome, user_id=user_id)
    db.session.add(category)
    db.session.commit()
    return category, None


def update_category(category_id, data):
    """
    Atualiza uma categoria existente.
    Retorna (category, None) em sucesso ou (None, mensagem_erro) em falha.
    """
    category = get_category_by_id(category_id)
    if not category:
        return None, "Categoria não encontrada."

    nome = data.get("nome")
    if nome is not None:
        if isinstance(nome, str):
            nome = nome.strip()
        if not nome:
            return None, "O campo 'nome' não pode ser vazio."
        category.nome = nome

    db.session.commit()
    return category, None


def delete_category(category_id):
    """
    Exclui uma categoria.
    Retorna (True, None) em sucesso ou (False, mensagem_erro) em falha.
    """
    category = get_category_by_id(category_id)
    if not category:
        return False, "Categoria não encontrada."

    db.session.delete(category)
    db.session.commit()
    return True, None
