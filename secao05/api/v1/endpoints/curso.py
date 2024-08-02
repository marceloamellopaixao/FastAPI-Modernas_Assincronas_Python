from typing import List

from fastapi import APIRouter
from fastapi import status
from fastapi import Depends
from fastapi import HTTPException
from fastapi import Response
from fastapi import Path

from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from secao05.models.curso_model import CursoModel  # Importa a Tabela Curso
from secao05.core.deps import get_session  # Recebe a conexão com o Banco de Dados

# Bypass warning SQLModel select
from sqlmodel.sql.expression import Select, SelectOfScalar

Select.inherit_cache = True  # Type: ignore
SelectOfScalar.inherit_cache = True  # Type: ignore
# Fim Bypass

router = APIRouter()


# POST Curso (Cria um curso)
@router.post('/', status_code=status.HTTP_201_CREATED, response_model=CursoModel, response_description='Curso criado com sucesso!',
             summary='Cria um Curso', description='Realiza o cadastro de um curso')
async def post_curso(curso: CursoModel, db: AsyncSession = Depends(get_session)):
    novo_curso = CursoModel(titulo=curso.titulo, aulas=curso.aulas, horas=curso.horas)

    db.add(novo_curso)
    await db.commit()

    return novo_curso


# GET Cursos (Retorna todos os cursos)
@router.get('/', status_code=status.HTTP_200_OK, response_model=List[CursoModel], response_description='Cursos encontrados com sucesso!',
            summary='Lista todos os Cursos', description='Realiza a listagem de todos os cursos')
async def get_cursos(db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(CursoModel)
        result = await session.execute(query)
        cursos: List[CursoModel] = result.scalars().all()

        return cursos


# GET Curso (Retorna somente um curso)
@router.get('/{curso_id}', status_code=status.HTTP_200_OK, response_model=CursoModel, response_description='O Curso foi encontrado com sucesso!',
            summary='Lista somente um curso pelo ID', description='Realiza a listagem do curso pelo ID mencionado')
async def get_curso(curso_id: int = Path(default=None, title='ID do Curso', gt=0), db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(CursoModel).filter(CursoModel.id == curso_id)
        result = await session.execute(query)
        curso: CursoModel = result.scalar_one_or_none()

        if curso:
            return curso
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Curso não encontrado!')


# PUT Curso (Atualiza os dados do curso pelo ID)
@router.put('/{curso_id}', status_code=status.HTTP_202_ACCEPTED, response_model=CursoModel, response_description='Curso atualizado com sucesso!',
            summary='Atualiza somente um curso pelo ID', description='Realiza a atualização do curso pelo ID mencionado')
async def put_curso(curso_id: int, curso: CursoModel, db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(CursoModel).filter(CursoModel.id == curso_id)
        result = await session.execute(query)
        curso_update: CursoModel = result.scalar_one_or_none()

        if curso_update:
            curso_update.titulo = curso.titulo
            curso_update.aulas = curso.aulas
            curso_update.horas = curso.horas
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Curso não encontrado!')


# DELETE Curso (Deleta o curso pelo ID)
@router.delete('/{curso_id}', status_code=status.HTTP_204_NO_CONTENT, response_description='Deletado com sucesso!',
               summary='Deleta somente um curso pelo ID', description='Realiza a exclusão do curso pelo ID mencionado')
async def delete_curso(curso_id: int, db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(CursoModel).filter(CursoModel.id == curso_id)
        result = await session.execute(query)
        curso_delete: CursoModel = result.scalar_one_or_none()

        if curso_delete:
            await session.delete(curso_delete)
            await session.commit()

            return Response(status_code=status.HTTP_204_NO_CONTENT)
        else:
            return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Curso não encontrado!')
