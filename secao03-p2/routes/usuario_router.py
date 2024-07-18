from fastapi import APIRouter

router = APIRouter()


@router.get('/api/v1/usuarios')  # Indica que o GET de todos os usuarios é no endpoint: Usuários
async def get_usuarios():
    return {'info': 'Todos os Usuários'}
