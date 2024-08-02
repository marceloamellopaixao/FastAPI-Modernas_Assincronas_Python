from typing import Optional
from pydantic import BaseModel, HttpUrl
# from pydantic import validator


class ArtigoSchema(BaseModel):
    id: Optional[int] = None
    titulo: str
    url_fonte: HttpUrl
    descricao: str
    usuario_id: Optional[int]

    class Config:
        orm_mode = True
