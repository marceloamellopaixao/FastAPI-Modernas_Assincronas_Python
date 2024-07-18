from fastapi import FastAPI

from secao04.core.configs import settings
from secao04.api.v1.api import api_router  # Importa o arquivo onde está o Endpoint (Curso)

app = FastAPI(
    title='Cursos API - FastAPI SQL Alchemy',
    description="Aprendendo a utilizar o FastAPI com Python + Banco de Dados para criar API's",
    version='0.0.1',
    contact={
        "name": "Marcelo Augusto M. Paixão",
        "url": "https://portmar.firebaseapp.com/",
        "email": "marceloamellopaixao@gmail.com"
    },
)

# Link da documentação será os seguintes: host:port/docs ou host:port/redoc
app.include_router(api_router, prefix=settings.API_V1_STR)  # Endpoint principal: host:port/api/v1/

if __name__ == '__main__':
    import uvicorn

    uvicorn.run(
        "main:app",
        host='0.0.0.0',
        port=8000,
        log_level='info',
        debug=True,
        reload=True
    )
