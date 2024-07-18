from fastapi import FastAPI
from fastapi import Query
from typing import Optional

app = FastAPI()


# Query Parameters
@app.get('/calculadora')
async def calcular(a: int = Query(default=None, gt=5), b: int = Query(default=None, gt=10), c: Optional[int] = None):
    soma: int = a + b
    if c:
        soma = soma + c

    return {"resultado": soma}


if __name__ == '__main__':
    import uvicorn

    uvicorn.run('query:app', host='0.0.0.0', port=8002, debug=True, reload=True)
