from dataclasses import dataclass
from typing import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession

from api.schema import WalletInfoSchema
from repository.models import WalletInfoModel
from services.converter import Converter


@dataclass
class RepositoryORM:
    converter: Converter
    session_factory: async_sessionmaker[AsyncSession]

    async def create(self, schema: WalletInfoSchema) -> WalletInfoSchema:
        try:
            model: WalletInfoModel = await self.converter.schema_to_model(schema)
            async with self.session_factory() as session:
                session.add(model)
                await session.commit()
                return await self.converter.model_to_schema(model)
        except Exception as e:
            await session.rollback()
            raise e

    async def get_with_pagination(
        self, offset: int, limit: int
    ) -> Sequence[WalletInfoSchema]:
        try:
            async with self.session_factory() as session:
                query = (
                    select(WalletInfoModel)
                    .order_by(WalletInfoModel.created_at.desc())
                    .offset(offset)
                    .limit(limit)
                )
                res = await session.execute(query)
                models = res.scalars().all()
                if models:
                    return await self.converter.models_seq_to_schema_seq(models=models)
                else:
                    return []
        except Exception as e:
            raise e
