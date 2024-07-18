# Instalação do FastAPI e Uvicorn: pip install fastapi uvicorn
# Execução da API: uvicorn main:app --reload (Recarrega sempre que houver alteração, não usar em produção).

# Instalação do Gunicorn (funciona somente em Linux e Mac): pip install gunicorn
# Execução da API com vários servidores: gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker

from fastapi import FastAPI

app = FastAPI()


@app.get('/')
async def raiz():
    return {"msg": "FastAPI na Geek University."}


if __name__ == '__main__':
    import uvicorn

    uvicorn.run('main:app', host='0.0.0.0', port=8000, log_level='info', reload=True)
    # 'main:app' (main é o nome do arquivo da aplicação : app é o nome do objeto FastAPI que roda a aplicação);
    # host='0.0.0.0' (Desta forma é possível verificar se a API está funcionando de diversos dispositivos locais);
    # port=8000 (É a porta em que a aplicação está rodando);
    # log_level='info' (Indica algumas informações da API enquanto está rodando);
    # reload=True (Recarrega sempre que houver alteração, não utilizar se estiver em produção).
