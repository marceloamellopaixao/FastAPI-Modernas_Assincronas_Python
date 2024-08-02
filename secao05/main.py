from fastapi import FastAPI

from secao05.core.configs import settings
from secao05.api.v1.api import api_router

app: FastAPI = FastAPI(title='Curso API - FastAPI SQLModel', version='0.0.1')
app.include_router(api_router, prefix=settings.API_V1_STR)

if __name__ == '__main__':
    import uvicorn

    uvicorn.run('main:app', host='0.0.0.0', port=8000, log_level='info', reload=True)
