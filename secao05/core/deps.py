from typing import Generator

from sqlalchemy.ext.asyncio import AsyncSession

from secao05.core.database import Session


async def get_session() -> Generator:
    session: AsyncSession = Session()

    try:
        yield session
    except Exception as error:
        print('Ocorreu o seguinte erro ao conectar,')
        print(error)
    finally:
        await session.close()
