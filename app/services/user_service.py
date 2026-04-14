from app import db
from app.models import User


def get_all_users():
    """Retorna todos os usuários."""
    return User.query.all()


def get_user_by_id(user_id):
    """Retorna um usuário pelo ID ou None."""
    return User.query.get(user_id)


def get_user_by_email(email):
    """Retorna um usuário pelo email ou None."""
    return User.query.filter_by(email=email).first()


def create_user(data):
    """
    Cria um novo usuário.
    Retorna (user, None) em sucesso ou (None, mensagem_erro) em falha.
    """
    nome = data.get("nome")
    email = data.get("email")

    if not nome or not email:
        return None, "Os campos 'nome' e 'email' são obrigatórios."

    nome = nome.strip()
    email = email.strip()

    if not nome or not email:
        return None, "Os campos 'nome' e 'email' não podem ser vazios."

    if get_user_by_email(email):
        return None, "Já existe um usuário com este email."

    user = User(nome=nome, email=email)
    db.session.add(user)
    db.session.commit()
    return user, None


def update_user(user_id, data):
    """
    Atualiza um usuário existente.
    Retorna (user, None) em sucesso ou (None, mensagem_erro) em falha.
    """
    user = get_user_by_id(user_id)
    if not user:
        return None, "Usuário não encontrado."

    nome = data.get("nome")
    email = data.get("email")

    if nome is not None:
        nome = nome.strip()
        if not nome:
            return None, "O campo 'nome' não pode ser vazio."
        user.nome = nome

    if email is not None:
        email = email.strip()
        if not email:
            return None, "O campo 'email' não pode ser vazio."
        existing = get_user_by_email(email)
        if existing and existing.id != user_id:
            return None, "Já existe um usuário com este email."
        user.email = email

    db.session.commit()
    return user, None


def delete_user(user_id):
    """
    Exclui um usuário.
    Retorna (True, None) em sucesso ou (False, mensagem_erro) em falha.
    """
    user = get_user_by_id(user_id)
    if not user:
        return False, "Usuário não encontrado."

    db.session.delete(user)
    db.session.commit()
    return True, None
