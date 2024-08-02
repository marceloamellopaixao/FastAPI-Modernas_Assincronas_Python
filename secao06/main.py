from fastapi import FastAPI

from secao06.core.configs import settings
from secao06.api.v1.api import api_router

app: FastAPI = FastAPI(title='Curso API - Segurança')
app.include_router(api_router, prefix=settings.API_V1_STR)

if __name__ == '__main__':
    import uvicorn

    uvicorn.run('main:app', host='0.0.0.0', port=8000, log_level='info', reload=True, debug=True)
