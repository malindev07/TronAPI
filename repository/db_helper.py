import asyncio
from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import (
    create_async_engine,
    AsyncEngine,
    async_sessionmaker,
    AsyncSession,
)
from repository.models.base import Base


class DataBaseHelper:

    def __init__(self, engine_url: str, db_echo: bool = False):
        self.engine_url: str = engine_url
        self.engine: AsyncEngine = create_async_engine(
            url=self.engine_url,
            echo=db_echo,
            pool_pre_ping=True,
        )
        self.session_factory = async_sessionmaker(
            bind=self.engine,
            class_=AsyncSession,
            autoflush=False,
            expire_on_commit=False,
        )

    async def init_db(self) -> None:
        async with self.engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)
            await conn.run_sync(Base.metadata.create_all)

    async def get_session(self) -> AsyncGenerator[AsyncSession, Exception]:
        try:
            async with self.session_factory() as session:
                yield session
        except Exception as e:
            raise e


db_helper = DataBaseHelper(engine_url="sqlite+aiosqlite:///database.db")
asyncio.run(db_helper.init_db())
# async def create_user():
#     async with db.session_factory() as session:
#         new_user = WalletInfo(
#             address="sdfsfsfdfs", balance=0.0, bandwidth=121241, energy=12414
#         )
#         session.add(new_user)
#         await session.commit()
#         return new_user
#
#
# asyncio.run(db.init_db())
# # asyncio.run(create_user())
