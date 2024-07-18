from fastapi import APIRouter

from secao04.api.v1.endpoints import curso

# Neste arquivo o intuito é fazer com que o roteamento seja fácil de localizar e bem identificado na Documentação da API

api_router = APIRouter()
api_router.include_router(curso.router, prefix='/cursos', tags=['cursos'])

# O Endpoint Completo da API ficará da seguinte forma: host:port/api/v1/cursos
