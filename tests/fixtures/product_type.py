import pytest

from src.models.models import ProductTypeDB

PRODUCT_TYPE = {
    'name': 'test',
}


async def create_types(override_get_async_session, count: int = 0):
    """Create a list of ProductType."""
    for _ in range(count):
        await create_type(override_get_async_session)


async def create_type(override_get_async_session):
    """Create a ProductType."""
    product = ProductTypeDB(**PRODUCT_TYPE)
    override_get_async_session.add(product)
    await override_get_async_session.commit()
    return product


@pytest.fixture(scope='function')
async def product_type(override_get_async_session):
    """Create a ProductType fixtures."""
    product_type = await create_type(override_get_async_session)
    await create_types(override_get_async_session, 10)
    return product_type


@pytest.fixture(scope='function')
async def type2(override_get_async_session):
    """Create a ProductType fixtures"""
    return await create_type(override_get_async_session)
