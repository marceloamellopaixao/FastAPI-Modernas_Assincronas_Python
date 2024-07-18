import json

from pydantic import BaseSettings
from sqlalchemy.ext.declarative import declarative_base

# É necessário criar um arquivo.json com os seguintes dados abaixo para que possa realizar a conexão com o banco de dados,
path = r"./credentials.json"

with open(path, 'r') as file:
    data = json.load(file)

user = data['user']  # Usuário do Banco de Dados
pswd = data['password']  # Senha do Banco de Dados
host = data['host']  # Host em que o Banco de Dados se encontra a conexão
port = data['port']  # Porta do Banco de Dados, por exemplo: 5432.
database = data['database']  # Nome do Banco de Dados que foi criado.


class Settings(BaseSettings):
    """
    Configurações Gerais usadas na aplicação.
    """

    API_V1_STR: str = "/api/v1"  # Endpoint padrão, alterar conforme a versão
    DB_URL: str = f"postgresql+asyncpg://{user}:{pswd}@{host}:{port}/{database}"  # Este é o SCRIPT de conexão entre BD e o Python
    DBBaseModel = declarative_base()  # Constrói uma classe base para definir as classes declarativas (Por exemplo: curso_model.py).

    class Config:
        case_sensitive = True


settings = Settings()
