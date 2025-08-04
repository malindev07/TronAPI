import os

import uvicorn
from contextlib import asynccontextmanager

from dotenv import load_dotenv
from fastapi import FastAPI
from api.handler import tron_router
from repository.db_helper import DataBaseHelper
from repository.repository_orm import RepositoryORM
from services.converter import Converter
from services.service import TronWalletService

load_dotenv()


@asynccontextmanager
async def lifespan(app: FastAPI):
    db_helper = DataBaseHelper(
        engine_url=f"{os.getenv("DB_NAME")}+{os.getenv("DB_ENGINE")}:///{os.getenv("DB_PATH")}"
    )
    
    await db_helper.init_db(is_drop=True if os.getenv("DB_DROP") == "1" else False)
    converter = Converter()
    repo = RepositoryORM(converter=converter, session_factory=db_helper.session_factory)
    service = TronWalletService(repo=repo)

    yield {"service": service}


app = FastAPI(lifespan=lifespan)

app.include_router(tron_router)
if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
