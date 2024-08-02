from typing import List, Optional, Any

from fastapi import APIRouter, status, Depends, HTTPException, Response
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import JSONResponse

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import IntegrityError

from secao06.models.usuario_model import UsuarioModel
from secao06.schemas.usuario_schema import UsuarioSchemaBase, UsuarioSchemaCreate, UsuarioSchemaUpdate, UsuarioSchemaArtigos

from secao06.core.deps import get_session, get_current_user
from secao06.core.security import gerar_hash_senha
from secao06.core.auth import autenticar, criar_token_acesso

router = APIRouter()


# GET Logado
@router.get('/logado', response_model=UsuarioSchemaBase)
def get_logado(usuario_logado: UsuarioModel = Depends(get_current_user)):
    return usuario_logado


# POST / SIGN-UP Usuário
@router.post('/signup', status_code=status.HTTP_201_CREATED,
             summary='',
             description='',
             response_model=UsuarioSchemaBase,
             response_description=''
             )
async def post_usuario(usuario: UsuarioSchemaCreate, db: AsyncSession = Depends(get_session)):
    novo_usuario: UsuarioModel = UsuarioModel(nome=usuario.nome, sobrenome=usuario.sobrenome,
                                              email=usuario.email,
                                              senha=gerar_hash_senha(usuario.senha),
                                              eh_admin=usuario.eh_admin)

    async with db as session:
        try:
            session.add(novo_usuario)
            await session.commit()

            return novo_usuario
        except IntegrityError:
            raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail='Já existe um usuário com este email cadastrado.')


# GET Usuários
@router.get('/', status_code=status.HTTP_200_OK,
            summary='',
            description='',
            response_model=List[UsuarioSchemaBase],
            response_description=''
            )
async def get_usuarios(db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(UsuarioModel)
        result = await session.execute(query)
        usuarios: List[UsuarioSchemaBase] = result.scalars().unique().all()

        if usuarios:
            return usuarios
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Não existe usuários!')


# GET Usuário
@router.get('/{usuario_id}', status_code=status.HTTP_200_OK,
            summary='',
            description='',
            response_model=UsuarioSchemaArtigos,
            response_description=''
            )
async def get_usuario(usuario_id: int, db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(UsuarioModel).filter(UsuarioModel.id == usuario_id)
        result = await session.execute(query)
        usuario: UsuarioSchemaArtigos = result.scalars().unique().one_or_none()

        if usuario:
            return usuario
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Usuário não encontrado!')


# PUT Usuário
@router.put('/{usuario_id}', status_code=status.HTTP_202_ACCEPTED,
            summary='',
            description='',
            response_model=UsuarioSchemaUpdate,
            response_description=''
            )
async def put_usuario(usuario_id: int, usuario: UsuarioSchemaUpdate, db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(UsuarioModel).filter(UsuarioModel.id == usuario_id)
        result = await session.execute(query)
        usuario_update: UsuarioSchemaBase = result.scalars().unique().one_or_none()

        if usuario:
            if usuario.nome:
                usuario_update.nome = usuario.nome
            if usuario.sobrenome:
                usuario_update.sobrenome = usuario.sobrenome
            if usuario.email:
                usuario_update.email = usuario.email
            if usuario.senha:
                usuario_update.senha = gerar_hash_senha(usuario.senha)
            if usuario.eh_admin:
                usuario_update.eh_admin = usuario.eh_admin

            await session.commit()

            return usuario
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Usuário não encontrado!')


# DELETE Usuário
@router.delete('/{usuario_id}', status_code=status.HTTP_204_NO_CONTENT,
               summary='',
               description=''
               )
async def delete_usuario(usuario_id: int, db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(UsuarioModel).filter(UsuarioModel.id == usuario_id)
        result = await session.execute(query)
        usuario_delete: UsuarioSchemaArtigos = result.scalars().unique().one_or_none()

        if usuario_delete:
            await session.delete(usuario_delete)
            await session.commit()

            return Response(status_code=status.HTTP_204_NO_CONTENT)
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Usuário não encontrado!')


# POST Login
@router.post('/login')
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_session)):
    usuario = await autenticar(email=form_data.username, senha=form_data.password, db=db)

    if not usuario:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Dados de Acesso Incorreto!!')

    return JSONResponse(content=
                        {
                            'access_token': criar_token_acesso(sub=usuario.id),
                            'token_type': 'bearer'
                         }, status_code=status.HTTP_200_OK)
