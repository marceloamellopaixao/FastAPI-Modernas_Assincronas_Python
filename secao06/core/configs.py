import json
from pydantic import BaseSettings
from sqlalchemy.ext.declarative import declarative_base

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
    DBBaseModel = declarative_base()

    JWT_SECRET: str = 'Iox1-WnYHuS9PNHMTTrWUhM613ih3WFF7zQJFPgH1n8'
    """
    import secrets
    
    token: str = secrets.token_urlsafe(32)
    """
    ALGORITHM: str = 'HS256'
    # O Tempo em minutos para expiração do Token (60 Minutos X 24 Horas X 7 Dias == 1 Semana)
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7

    class Config:
        case_sensitive = True


settings: Settings = Settings()
