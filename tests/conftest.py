import random
from typing import AsyncGenerator

import pytest
from sqlalchemy import StaticPool, event
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from src.base.models import BaseDBModel
from src.config.session import get_async_session
from src.config.settings import config
from src.main import app


pytest_plugins = [
    'tests.fixtures.product_type',
    'tests.fixtures.product',
]


def get_random_value(length: int = 10) -> str:
    """Function to get a random value."""
    value = random.randint(0, 10 ** length - 1)
    return f'{value:0{length}}'


def get_url_size(url: str, size: int, page: int = None) -> str:
    """Function to get pagination settings in an address."""
    url = f'{url}?size={size}'
    if page:
        url += f'&page={page}'
    return url


engine_test = create_async_engine(config.database.test_sqlite_db_url, connect_args={'check_same_thread': False},
                                  poolclass=StaticPool)
event.listen(engine_test.sync_engine, 'connect', lambda c, _: c.execute('pragma foreign_keys=on'))
async_session_maker = async_sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine_test,
    class_=AsyncSession,
    expire_on_commit=False,
)


async def override_async_session() -> AsyncGenerator[AsyncSession, None]:
    """Function to override asynchronous session."""
    async with async_session_maker() as session:
        try:
            yield session
        finally:
            await session.close()


app.dependency_overrides[get_async_session] = override_async_session


@pytest.fixture(scope='function')
async def override_get_async_session() -> AsyncGenerator[AsyncSession, None]:
    """Fixture for overriding asynchronous session."""
    async with async_session_maker() as session:
        try:
            yield session
        finally:
            await session.close()


@pytest.fixture(autouse=True, scope='function')
async def prepare_database():
    """Fixture for connecting to a database."""
    async with engine_test.begin() as conn:
        await conn.run_sync(BaseDBModel.metadata.create_all)
    yield
    async with engine_test.begin() as conn:
        await conn.run_sync(BaseDBModel.metadata.drop_all)
