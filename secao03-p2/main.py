from fastapi import FastAPI

from routes import curso_router, usuario_router

app = FastAPI()
app.include_router(curso_router.router, tags=['Cursos'])  # Unifica todas as rotas no main por classificação de Cursos na Documentação da API.
app.include_router(usuario_router.router, tags=['Usuários'])  # Unifica todas as rotas no main por classificação de Usuários na Documentação da API.


if __name__ == '__main__':
    import uvicorn

    uvicorn.run('main:app', host='0.0.0.0', port=8000, debug=True, reload=True)
