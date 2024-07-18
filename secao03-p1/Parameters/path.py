from fastapi import FastAPI
from fastapi import HTTPException
from fastapi import Path
from fastapi import status

app = FastAPI()

cursos = {
    1: {
        "titulo": "HTML Básico",
        "aulas": 30,
        "horas": 24
    },
    2: {
        "titulo": "CSS Básico",
        "aulas": 20,
        "horas": 18
    },
    3: {
        "titulo": "JavaScript Básico",
        "aulas": 60,
        "horas": 50
    }
}

# Requisição GET (READ BY ID)
"""
No parâmetro PATH tem os seguintes dados,

Less Than << LT >> Menor do que ...
Less Than or Equal to << LE >> Menor ou igual a...
Greater Than << GT >> Maior do que ...
Greater Than or Equal to << GE >> Maior ou igual a...
"""


@app.get('/cursos/{curso_id}', status_code=status.HTTP_200_OK)
async def get_curso(
        curso_id: int = Path(default=None, title='ID do curso', description='Deve ser entre 1 à 3', gt=0, lt=4)):
    try:
        curso = cursos[curso_id]
        return curso

    except KeyError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Curso não encontrado.')

if __name__ == '__main__':
    import uvicorn

    uvicorn.run('path:app', host='0.0.0.0', port=8001, debug=True, reload=True)
