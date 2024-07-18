import json

from pydantic import BaseSettings
from sqlalchemy.ext.declarative import declarative_base

path = r"./credentials.json"

with open(path, 'r') as file:
    data = json.load(file)

user = data['user']
pswd = data['password']
host = data['host']
port = data['port']
database = data['database']


class Settings(BaseSettings):
    """
    Configurações Gerais usadas na aplicação.
    """

    API_V1_STR: str = "/api/v1"
    DB_URL: str = f"postgresql+asyncpg://{user}:{pswd}@{host}:{port}/{database}"
    DBBaseModel = declarative_base()

    class Config:
        case_sensitive = True


settings = Settings()
