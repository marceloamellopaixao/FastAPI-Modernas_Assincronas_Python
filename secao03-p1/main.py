from typing import Dict, List, Optional, Any

from fastapi.responses import JSONResponse
from fastapi import Response
from fastapi import Path
from fastapi import Query
from fastapi import Header

from fastapi import FastAPI
from fastapi import HTTPException
from fastapi import status
from fastapi import Depends

from time import sleep

from models import Curso
from models import cursos


def fake_db():
    try:
        print('Abrindo conexão com banco de dados...')
        sleep(1)
    except:
        ...
    finally:
        print('Fechando conexão com banco de dados...')
        sleep(1)


app = FastAPI(
    title='API de Cursos da Geek University',
    description='FastAPI com Python',
    version='0.0.1',
    docs_url='/docs-api',
    redoc_url='/redoc-api'
    )


# Requisição GET (READ ALL)
@app.get('/cursos', tags=['Cursos'],
         description='Retorna todos os cursos ou uma lista vazia.',
         summary='Retorna todos os cursos',
         response_description='Cursos encontrados com Sucesso!',
         response_model=List[Curso]
         )
async def get_cursos(db: Any = Depends(fake_db)):
    return cursos


# Requisição GET (READ BY ID)
@app.get('/cursos/{curso_id}', tags=['Cursos'],
         description='Retorna um curso por Identificação (ID)',
         summary='Retorna um por ID',
         response_description='Curso encontrado com Sucesso!'
         )
async def get_curso(
        curso_id: int = Path(default=None, title='ID do curso', description='Deve ser maior que 0', gt=0),
        db: Any = Depends(fake_db)):
    try:
        curso = cursos[curso_id]
        return curso

    except KeyError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Curso não encontrado.')
    except IndexError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Curso não encontrado.')


# Requisição POST (CREATE)
@app.post('/cursos', status_code=status.HTTP_201_CREATED, tags=['Cursos'],
          description='Cria um curso e adiciona na lista',
          summary='Cria um curso',
          response_model=Curso)
async def post_curso(curso: Curso, db: Any = Depends(fake_db)):
    try:
        # Verifica se o ID já existe e acrescenta 1 para criar um novo curso
        next_id: int = len(cursos) + 1
        curso.id = next_id
        cursos.append(curso)
        return curso

    except Exception as a:
        print('Erro:', a)
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f'Curso com o ID {curso.id}, já existente!')


# Requisição PUT (UPDATE)
@app.put('/cursos/{curso_id}', status_code=status.HTTP_200_OK, tags=['Cursos'])
async def put_curso(curso_id: int, curso: Curso, db: Any = Depends(fake_db)):
    if curso_id in cursos:
        cursos[curso_id] = curso
        # del curso.id
        return curso

    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Não existe este curso com ID {curso_id}.')


# Requisição DELETE (DELETAR/APAGAR)
@app.delete('/cursos/{curso_id}', tags=['Cursos'])
async def delete_curso(curso_id: int, db: Any = Depends(fake_db)):
    if curso_id in cursos:
        del cursos[curso_id]  # Deleta o curso pela ID.
        # Não funciona, porque há um bug no código da FastAPI na versão que o professor solicitou (fastapi==0.75.2)
        # Testar com a versão atual e verificar se executa com sucesso.
        # return JSONResponse(status_code=status.HTTP_204_NO_CONTENT)
        return Response(status_code=status.HTTP_204_NO_CONTENT)

    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Não existe este curso com ID {curso_id}.')


# Query Parameters
@app.get('/calculadora', tags=['Calculadora'])
async def calcular(a: int = Query(default=None, gt=5), b: int = Query(default=None, gt=10),
                   x_geek: str = Header(default=None), c: Optional[int] = None):
    soma: int = a + b
    if c:
        soma = soma + c

    print('X-GEEK: ', x_geek)
    return {"resultado": soma}


if __name__ == '__main__':
    import uvicorn

    uvicorn.run('main:app', host='0.0.0.0', port=8000, debug=True, reload=True)
