from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from httpx import AsyncClient
from tronpy import AsyncTron

from api.handler import tron_router
from services.service import TronWalletService


@asynccontextmanager
async def lifespan(app: FastAPI):
    service = TronWalletService(_url="https://apilist.tronscanapi.com/api")

    yield {"service": service}


app = FastAPI(lifespan=lifespan)

app.include_router(tron_router)
if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
