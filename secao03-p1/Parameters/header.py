from fastapi import FastAPI
from fastapi import Query, Header
from typing import Optional

app = FastAPI()


# Header Parameters
@app.get('/calculadora')
async def calcular(a: int = Query(default=None, gt=5), b: int = Query(default=None, gt=10), x_geek: str = Header(default=None), c: Optional[int] = None):
    soma: int = a + b
    if c:
        soma = soma + c

    print(f'X-GEEK: {x_geek}')
    return {"resultado": soma}


if __name__ == '__main__':
    import uvicorn

    uvicorn.run('header:app', host='0.0.0.0', port=8003, debug=True, reload=True)
