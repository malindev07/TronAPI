import pytest
from sqlalchemy import select
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession

from api.schema import WalletInfoSchema
from repository.models import WalletInfoModel
from repository.repository_orm import RepositoryORM
from services.converter import Converter


@pytest.mark.asyncio
async def test_save_in_db(db_session_factory: async_sessionmaker[AsyncSession]) -> None:
    addr = "TQAXVqxCHPGEAQMn945kta22FUicd28SLo"
    converter = Converter()
    repo = RepositoryORM(converter=converter, session_factory=db_session_factory)
    schema = WalletInfoSchema(
        address=addr, balance=111.1111, bandwidth=1234, energy=11111111
    )

    await repo.create(schema)
    async with db_session_factory() as session:
        result = await session.execute(
            select(WalletInfoModel).where(WalletInfoModel.address == addr)
        )
        model = result.scalar_one()
        assert model is not None
        assert model.address == schema.address
        assert model.balance == schema.balance
        assert model.energy == schema.energy
        assert model.bandwidth == schema.bandwidth
