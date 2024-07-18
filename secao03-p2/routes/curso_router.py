from fastapi import APIRouter

router = APIRouter()


@router.get('/api/v1/cursos')  # Indica que o GET de todos os cursos é no endpoint: Cursos
async def get_cursos():
    return {'info': 'Todos os cursos'}
