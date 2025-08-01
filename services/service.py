from dataclasses import dataclass
from httpx import AsyncClient
from api.schema import WalletInfoSchema


# @dataclass
# class WalletInfo:
#     addr: str
#     balance: float = 0.0
#     bandwidth: int = 0
#     energy: int = 0


@dataclass
class TronWalletService:
    _url: str

    async def get_bandwidth_energy_balance(self, addr: str) -> WalletInfoSchema:
        # TODO Уточнить у коуча
        async with AsyncClient() as client:
            response = await client.get(url=f"{self._url}/accountv2?address={addr}")
            params = response.json()

            wi = WalletInfoSchema(
                address=addr, balance=float(params["balance"] / 1000000)
            )

            if "netUsed" in params["bandwidth"] and "netLimit" in params["bandwidth"]:
                wi.bandwidth = (
                    int(params["bandwidth"]["netLimit"])
                    - int(params["bandwidth"]["netUsed"])
                    + (
                        int(params["bandwidth"]["freeNetLimit"])
                        - int(params["bandwidth"]["freeNetUsed"])
                    )
                )
            if (
                "energyUsed" in params["bandwidth"]
                and "energyLimit" in params["bandwidth"]
            ):
                energy = int(params["bandwidth"]["energyLimit"]) - int(
                    params["bandwidth"]["energyUsed"]
                )
                if energy < 0:
                    wi.energy = 0
                else:
                    wi.energy = energy
            return wi
