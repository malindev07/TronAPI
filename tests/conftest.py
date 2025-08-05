from typing import AsyncGenerator, Any

import pytest_asyncio
from contextlib import asynccontextmanager
from fastapi import FastAPI
import httpx
from asgi_lifespan import LifespanManager
from httpx import ASGITransport
from sqlalchemy.ext.asyncio import (
    create_async_engine,
    async_sessionmaker,
    AsyncSession,
    AsyncEngine,
)

from api.handler import tron_router
from repository.db_helper import DataBaseHelper
from repository.models.base import Base
from repository.repository_orm import RepositoryORM
from services.converter import Converter
from services.service import TronWalletService


@pytest_asyncio.fixture
async def app() -> AsyncGenerator:
    db_helper = DataBaseHelper(engine_url="sqlite+aiosqlite:///:memory:")
    await db_helper.init_db(is_drop=True)
    converter = Converter()
    repo = RepositoryORM(converter=converter, session_factory=db_helper.session_factory)
    service = TronWalletService(repo=repo)

    @asynccontextmanager
    async def lifespan(app: FastAPI):
        yield {"service": service}

    app = FastAPI(lifespan=lifespan)
    app.include_router(tron_router)

    async with LifespanManager(app) as manager:
        yield manager.app


@pytest_asyncio.fixture
async def client(app):
    async with httpx.AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        yield client


@pytest_asyncio.fixture
async def db_engine() -> AsyncGenerator[AsyncEngine, Any]:
    engine = create_async_engine("sqlite+aiosqlite:///:memory:")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield engine
    await engine.dispose()


@pytest_asyncio.fixture
async def db_session_factory(
    db_engine: AsyncEngine,
) -> async_sessionmaker[AsyncSession]:
    return async_sessionmaker(db_engine, expire_on_commit=False)
