from dataclasses import dataclass
from typing import Sequence

from httpx import AsyncClient
from api.schema import WalletInfoSchema, WalletNotFoundSchema
from repository.repository_orm import RepositoryORM


@dataclass
class WalletParamsAttrs:
    balance: str = "balance"
    bandwidth: str = "bandwidth"
    netUsed: str = "netUsed"
    netLimit: str = "netLimit"
    freeNetLimit: str = "freeNetLimit"
    freeNetUsed: str = "freeNetUsed"
    energyLimit: str = "energyLimit"
    energyUsed: str = "energyUsed"


@dataclass
class TronWalletService:
    repo: RepositoryORM
    _url: str = "https://apilist.tronscanapi.com/api"

    async def check_bandwidth_energy_balance(
        self, addr: str
    ) -> WalletInfoSchema | WalletNotFoundSchema:
        async with AsyncClient() as client:
            response = await client.get(url=f"{self._url}/accountv2?address={addr}")
            params = response.json()
            if not params:
                return WalletNotFoundSchema(address=addr)

            wi = WalletInfoSchema(
                address=addr,
                balance=float(params[WalletParamsAttrs.balance] / 1000000),
            )

            if (
                WalletParamsAttrs.netUsed in params[WalletParamsAttrs.bandwidth]
                and WalletParamsAttrs.netLimit in params[WalletParamsAttrs.bandwidth]
            ):
                wi.bandwidth = (
                    int(params[WalletParamsAttrs.bandwidth][WalletParamsAttrs.netLimit])
                    - int(
                        params[WalletParamsAttrs.bandwidth][WalletParamsAttrs.netUsed]
                    )
                    + (
                        int(
                            params[WalletParamsAttrs.bandwidth][
                                WalletParamsAttrs.freeNetLimit
                            ]
                        )
                        - int(
                            params[WalletParamsAttrs.bandwidth][
                                WalletParamsAttrs.freeNetUsed
                            ]
                        )
                    )
                )
            if (
                WalletParamsAttrs.energyUsed in params[WalletParamsAttrs.bandwidth]
                and WalletParamsAttrs.energyLimit in params[WalletParamsAttrs.bandwidth]
            ):
                energy = int(
                    params[WalletParamsAttrs.bandwidth][WalletParamsAttrs.energyLimit]
                ) - int(
                    params[WalletParamsAttrs.bandwidth][WalletParamsAttrs.energyUsed]
                )
                if energy < 0:
                    wi.energy = 0
                else:
                    wi.energy = energy

            return await self.repo.create(wi)

    async def get_with_pagination(
        self, offset: int, limit: int
    ) -> Sequence[WalletInfoSchema]:
        return await self.repo.get_with_pagination(offset=offset, limit=limit)
