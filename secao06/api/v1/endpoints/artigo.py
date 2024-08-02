from typing import List

from fastapi import APIRouter, status, Depends, HTTPException, Response

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from secao06.models.artigo_model import ArtigoModel  # Modelo dos Dados do Artigo
from secao06.models.usuario_model import UsuarioModel  # Modelo dos Dados de Usuário
from secao06.schemas.artigo_schema import ArtigoSchema  # Schema - Tabela do Banco de Dados
from secao06.core.deps import get_session, get_current_user

router = APIRouter()


# POST Artigo
@router.post('/', status_code=status.HTTP_201_CREATED,
             summary='Cria um Artigo',
             description='Realiza a criação do Artigo e Salva no BD!',
             response_model=ArtigoSchema,
             response_description='O Artigo foi criado com sucesso!'
             )
async def post_artigo(artigo: ArtigoSchema, usuario_logado: UsuarioModel = Depends(get_current_user), db: AsyncSession = Depends(get_session)):
    novo_artigo: ArtigoModel = ArtigoModel(titulo=artigo.titulo, descricao=artigo.descricao, url_fonte=artigo.url_fonte, usuario_id=usuario_logado.id)

    db.add(novo_artigo)
    await db.commit()

    return novo_artigo


# GET Artigos
@router.get('/', status_code=status.HTTP_200_OK,
            summary='',
            description='',
            response_model=List[ArtigoSchema],
            response_description=''
            )
async def get_artigos(db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(ArtigoModel)
        result = await session.execute(query)
        artigos: List[ArtigoModel] = result.scalars().unique().all()

        return artigos


# GET Artigo
@router.get('/{artigo_id}', status_code=status.HTTP_200_OK,
            summary='',
            description='',
            response_model=ArtigoSchema,
            response_description=''
            )
async def get_artigo(artigo_id: int, db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(ArtigoModel).filter(ArtigoModel.id == artigo_id)
        result = await session.execute(query)
        artigo: ArtigoModel = result.scalars().unique().one_or_none()

        if artigo:
            return artigo
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Artigo não encontrado!')


# PUT Artigo
@router.put('/{artigo_id}', status_code=status.HTTP_202_ACCEPTED,
            summary='',
            description='',
            response_model=ArtigoSchema,
            response_description=''
            )
async def put_artigo(artigo_id: int, artigo: ArtigoSchema, db: AsyncSession = Depends(get_session), usuario_logado: UsuarioModel = Depends(get_current_user)):
    async with db as session:
        query = select(ArtigoModel).filter(ArtigoModel.id == artigo_id)
        result = await session.execute(query)
        artigo_update: ArtigoModel = result.scalars().unique().one_or_none()

        if artigo_update:
            if artigo.titulo:
                artigo_update.titulo = artigo.titulo

            if artigo.descricao:
                artigo_update.descricao = artigo.descricao

            if artigo.url_fonte:
                artigo_update.url_fonte = artigo.url_fonte

            if usuario_logado.id != artigo_update.usuario_id:
                artigo_update.usuario_id = usuario_logado.id

            await session.commit()
            return artigo_update
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Artigo não encontrado!')


# DELETE Artigo
@router.delete('/{artigo_id}', status_code=status.HTTP_202_ACCEPTED,
               summary='',
               description=''
               )
async def delete_artigo(artigo_id: int, db: AsyncSession = Depends(get_session), usuario_logado: UsuarioModel = Depends(get_current_user)):
    async with db as session:
        query = select(ArtigoModel
                       ).filter(ArtigoModel.id == artigo_id
                                ).filter(ArtigoModel.usuario_id == usuario_logado.id)  # Somente o usuário que criou o artigo consegue deletar
        result = await session.execute(query)
        artigo_delete: ArtigoModel = result.scalars().unique().one_or_none()

        if artigo_delete:
            await session.delete(artigo_delete)
            await session.commit()
            return Response(status_code=status.HTTP_204_NO_CONTENT)
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Artigo não encontrado!')
