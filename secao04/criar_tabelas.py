from secao04.core.configs import settings
from secao04.core.database import engine


# Realiza a criação das tabelas.
async def create_tables() -> None:
    import models.__all_models
    print("Criando as tabelas no Banco de Dados...")

    async with engine.begin() as conn:
        await conn.run_sync(settings.DBBaseModel.metadata.drop_all)
        await conn.run_sync(settings.DBBaseModel.metadata.create_all)
    print('Tabelas criadas com sucesso!')

if __name__ == '__main__':
    import asyncio
    asyncio.run(create_tables())
