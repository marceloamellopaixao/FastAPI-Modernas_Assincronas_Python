import json

from pydantic import BaseSettings

path = r"./credentials.json"

with open(path, 'r') as file:
    data = json.load(file)

user = data['user']  # Usuário do Banco de Dados
pswd = data['password']  # Senha do Banco de Dados
host = data['host']  # Host em que o Banco de Dados se encontra a conexão
port = data['port']  # Porta do Banco de Dados, por exemplo: 5432.
database = data['database']  # Nome do Banco de Dados que foi criado.


class Settings(BaseSettings):
    API_V1_STR: str = '/api/v1'
    DB_URL: str = f'postgresql+asyncpg://{user}:{pswd}@{host}:{port}/{database}'

    class Config:
        case_sensitive = True


settings: Settings = Settings()
