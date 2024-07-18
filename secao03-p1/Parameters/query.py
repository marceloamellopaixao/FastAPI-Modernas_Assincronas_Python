from fastapi import FastAPI
from fastapi import Query
from typing import Optional

app = FastAPI()

"""
Less Than << LT >> Menor do que ...
Less Than or Equal to << LE >> Menor ou igual a...
Greater Than << GT >> Maior do que ...
Greater Than or Equal to << GE >> Maior ou igual a...
"""

# Query Parameters
# Demonstra qual dado irá receber informação via Query e não Body (Exemplo: JSON)
@app.get('/calculadora')
async def calcular(a: int = Query(default=None, gt=5), b: int = Query(default=None, gt=10), c: Optional[int] = None):
    soma: int = a + b
    if c:
        soma = soma + c

    return {"resultado": soma}


if __name__ == '__main__':
    import uvicorn

    uvicorn.run('query:app', host='0.0.0.0', port=8002, debug=True, reload=True)
