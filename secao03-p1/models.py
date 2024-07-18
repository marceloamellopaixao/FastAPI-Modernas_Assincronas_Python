from typing import Optional
from pydantic import BaseModel, validator


class Curso(BaseModel):
    id: Optional[int] = None
    titulo: str
    aulas: int
    horas: int

    @validator('titulo')
    def validar_titulo(cls, value: str):
        # Validação de Palavra
        palavras = value.split(' ')
        if len(palavras) < 3:
            raise ValueError('O título deve conter pelo menos 3 palavras.')

        # Validação se o titulo é minusculo ou maiusculo
        if value.islower() or value.isupper():
            raise ValueError('O título deve ser capitalizado.')
        return value

    @validator('aulas')
    def validar_aulas(cls, value: int):
        # Validação se a quantidade de aulas é maior que 12
        if value <= 12:
            raise ValueError('A quantidade de aulas tem de ser maior que 12!')
        return value

    @validator('horas')
    def validar_horas(cls, value: int):
        # Validação se a quantidade de horas é maior que 10
        if value <= 10:
            raise ValueError('A quantidade de horas do curso tem de ser maior que 10!')
        return value


cursos = [
    Curso(id=1, titulo='HTML Básico ao Avançado', aulas=30, horas=24),
    Curso(id=2, titulo='CSS Básico ao Avançado', aulas=20, horas=18),
    Curso(id=3, titulo='JavaScript Básico ao Avançado', aulas=60, horas=30)
]

cursos_dict = {
    1: {
        "id": 1,
        "titulo": "HTML Básico",
        "aulas": 30,
        "horas": 24
    },
    2: {
        "id": 2,
        "titulo": "CSS Básico",
        "aulas": 20,
        "horas": 18
    },
    3: {
        "id": 3,
        "titulo": "JavaScript Básico",
        "aulas": 60,
        "horas": 50
    }
}