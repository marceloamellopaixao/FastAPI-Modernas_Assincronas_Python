from typing import List
from fastapi import APIRouter
from fastapi import status
from fastapi import Depends
from fastapi import HTTPException
from fastapi import Response

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from secao04.models.curso_model import CursoModel
from secao04.schemas.curso_schema import CursoSchema
from secao04.core.deps import get_session

router = APIRouter()
# Neste arquivo é realizada a separação do roteamento de cada endpoint para que o código não fique bagunçado em somente um arquivo.

# POST Curso (Cria o Curso)
@router.post(
    '/',
    summary='Cadastra um curso',
    description='Realiza o cadastro do curso no Banco de Dados',
    response_description='Cadastro do curso foi realizado com sucesso!',
    response_model=CursoSchema,
    status_code=status.HTTP_201_CREATED
)
async def post_curso(curso: CursoSchema, db: AsyncSession = Depends(get_session)):
    novo_curso = CursoModel(
        titulo=curso.titulo,
        aulas=curso.aulas,
        horas=curso.horas
    )

    db.add(novo_curso)
    await db.commit()

    return novo_curso


# GET Cursos (Lista todos os cursos cadastrados)
@router.get(
    '/',
    summary='Retorna todos os cursos',
    description='Realiza a consulta e retorno de todos os cursos cadastrados',
    response_description='Todos os cursos foram encontrados com sucesso!',
    response_model=List[CursoSchema],
    status_code=status.HTTP_200_OK
)
async def get_cursos(db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(CursoModel)
        result = await session.execute(query)
        cursos: List[CursoModel] = result.scalars().all()

        return cursos


# GET Curso (Lista um curso cadastrado)
@router.get(
    '/{curso_id}',
    summary='Retorna um curso pelo ID',
    description='Realiza a consulta e retorno de somente um dos cursos cadastrados pelo ID',
    response_description='Curso encontrado com sucesso!',
    response_model=CursoSchema,
    status_code=status.HTTP_200_OK
)
async def get_curso(curso_id: int, db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(CursoModel).filter(CursoModel.id == curso_id)
        result = await session.execute(query)
        curso: List[CursoModel] = result.scalar_one_or_none()

        if curso:
            return curso
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Curso não encontrado')


# PUT Curso (Atualiza o curso cadastrado)
@router.put(
    '/{curso_id}',
    summary='Atualiza um Curso',
    description='Realiza a atualização do curso.',
    response_description='Curso atualizado com Sucesso!',
    response_model=CursoSchema,
    status_code=status.HTTP_202_ACCEPTED
)
async def put_curso(curso_id: int, curso: CursoSchema, db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(CursoModel).filter(CursoModel.id == curso_id)
        result = await session.execute(query)
        curso_up: List[CursoModel] = result.scalar_one_or_none()

        if curso_up:
            curso_up.titulo = curso.titulo
            curso_up.aulas = curso.aulas
            curso_up.horas = curso.horas

            await session.commit()

            return curso_up
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Curso não encontrado')


# DELETE Curso (Deleta o curso cadastrado)
@router.delete(
    '/{curso_id}',
    summary='Deleta um curso',
    description='Deleta o curso especificado pelo ID do Banco de Dados.',
    response_description='Curso deletado com sucesso!',
    status_code=status.HTTP_204_NO_CONTENT
)
async def delete_curso(curso_id: int, db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(CursoModel).filter(CursoModel.id == curso_id)
        result = await session.execute(query)
        curso_del: List[CursoModel] = result.scalar_one_or_none()

        if curso_del:
            await session.delete(curso_del)
            await session.commit()

            return Response(status_code=status.HTTP_204_NO_CONTENT)
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Curso não encontrado')
