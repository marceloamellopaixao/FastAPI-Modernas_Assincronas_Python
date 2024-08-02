from passlib.context import CryptContext


CRYPTO = CryptContext(schemes=['bcrypt'], deprecated='auto')


def verificar_senha(senha: str, hash_senha: str) -> bool:
    """
    Função para verificar se a senha está correta, comparando a senha em texto puro,
    informada pelo usuário e o hash da senha que estará salvo no banco de dados durante a criação da conta.
    :param senha:
    :param hash_senha:
    :return: Retorna se é válido ou não a senha
    """
    return CRYPTO.verify(senha, hash_senha)


def gerar_hash_senha(senha: str) -> str:
    """
    Função que gera e retorna o hash da senha
    :param senha:
    :return: Retorna o Hash da senha que o usuário criou
    """
    return CRYPTO.hash(senha)
