from typing import Optional
from typing import List

from pydantic import BaseModel, EmailStr
from pydantic import validator

from secao06.schemas.artigo_schema import ArtigoSchema


class UsuarioSchemaBase(BaseModel):
    id: Optional[int] = None
    nome: str
    sobrenome: str
    email: EmailStr
    eh_admin: bool = False

    class Config:
        orm_mode = True


class UsuarioSchemaCreate(UsuarioSchemaBase):
    senha: str

    # Validação de Entrada da Senha
    @validator('senha')
    def validar_senha(cls, value: str):
        if len(value) <= 0:
            raise ValueError('Senha tem que ser preenchida!')

        if len(value) <= 7:
            raise ValueError('Senha deve conter 8 caracteres ou mais')

        return value


class UsuarioSchemaArtigos(UsuarioSchemaBase):
    artigos: Optional[List[ArtigoSchema]]


class UsuarioSchemaUpdate(UsuarioSchemaBase):
    nome: Optional[str]
    sobrenome: Optional[str]
    email: Optional[EmailStr]
    senha: Optional[str]
    eh_admin: Optional[bool]

