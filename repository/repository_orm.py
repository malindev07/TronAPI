import asyncio
from dataclasses import dataclass

from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession

from repository.db_helper import db_helper
from repository.models import WalletInfo


@dataclass
class RepositoryORM:
    session_factory: async_sessionmaker[AsyncSession] = db_helper.session_factory

    async def create(self, model: WalletInfo):
        try:
            async with self.session_factory() as session:
                session.add(model)
                await session.commit()
        except Exception as e:
            await session.rollback()
            raise e
        return model


# a = RepositoryORM()
# asyncio.run(
#     a.create(
#         WalletInfo(address="sdfsfsfdfs", balance=0.0, bandwidth=121241, energy=12414)
#     )
# )
