from fastapi import APIRouter, Request, Query

from api.schema import WalletInfoSchema

tron_router = APIRouter(prefix="/wallet", tags=["Tron Wallet Parameters"])


@tron_router.post("/info")
async def get_bandwidth_energy_balance(
    request: Request, address: str = Query(..., regex=r"^T[a-zA-Z0-9]{33}$")
) -> WalletInfoSchema:

    return await request.state.service.get_bandwidth_energy_balance(addr=address)
