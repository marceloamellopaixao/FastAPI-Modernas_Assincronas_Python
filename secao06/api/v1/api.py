from fastapi import APIRouter
from secao06.api.v1.endpoints import artigo, usuario

api_router = APIRouter()

api_router.include_router(artigo.router, prefix='/artigos', tags=['artigos'])
api_router.include_router(usuario.router, prefix='/usuarios', tags=['usuarios'])
