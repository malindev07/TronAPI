from dataclasses import dataclass
from typing import Sequence

from api.schema import WalletInfoSchema
from repository.models import WalletInfoModel


@dataclass
class Converter:

    async def schema_to_model(self, schema: WalletInfoSchema) -> WalletInfoModel:
        return WalletInfoModel(
            address=schema.address,
            balance=schema.balance,
            bandwidth=schema.bandwidth,
            energy=schema.energy,
        )

    async def model_to_schema(self, model: WalletInfoModel) -> WalletInfoSchema:

        return WalletInfoSchema(
            address=model.address,
            balance=model.balance,
            bandwidth=model.bandwidth,
            energy=model.energy,
        )

    async def models_seq_to_schema_seq(
        self, models: Sequence[WalletInfoModel]
    ) -> Sequence[WalletInfoSchema]:
        schemas = []
        for model in models:
            schemas.append(await self.model_to_schema(model))

        return schemas
