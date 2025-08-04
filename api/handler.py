import json
from typing import Sequence

from fastapi import APIRouter, Request, Query, Response

from api.schema import WalletInfoSchema, WalletNotFoundSchema

tron_router = APIRouter(prefix="/wallet", tags=["Tron Wallet Resources"])


@tron_router.post("/resources", response_class=Response)
async def check_bandwidth_energy_balance(
    request: Request, address: str = Query(..., pattern=r"^T[a-zA-Z0-9]{33}$")
) -> Response:
    res = await request.state.service.check_bandwidth_energy_balance(addr=address)
    if isinstance(res, WalletNotFoundSchema):
        return Response(
            status_code=404,
            content=res.model_dump_json(),
            media_type="application/json",
        )
    return Response(
        status_code=200,
        content=res.model_dump_json(),
        media_type="application/json",
    )


@tron_router.get("/", response_class=Response)
async def get_with_pagination(
    request: Request,
    offset: int = Query(default=0, ge=0, le=10),
    limit: int = Query(default=10, ge=1, le=100),
) -> Response:
    return Response(
        content=json.dumps(
            [
                item.model_dump()
                for item in await request.state.service.get_with_pagination(
                    offset=offset, limit=limit
                )
            ]
        ),
        status_code=200,
        media_type="application/json",
    )
