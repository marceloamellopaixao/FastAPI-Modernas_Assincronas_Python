from secao04.core.configs import settings
from sqlalchemy import Column, Integer, String

# Cria um Modelo de tabela que será criada no Banco


class CursoModel(settings.DBBaseModel):
    __tablename__ = 'cursos'

    id: int = Column(Integer, primary_key=True, autoincrement=True)
    titulo: str = Column(String(100))
    aulas: int = Column(Integer)
    horas: int = Column(Integer)
