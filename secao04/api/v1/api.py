from fastapi import APIRouter

from secao04.api.v1.endpoints import curso

api_router = APIRouter()
api_router.include_router(curso.router, prefix='/cursos', tags=['cursos'])

# Endpoint Completo: host/api/v1/cursos:port
