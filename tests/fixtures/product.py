import pytest

from src.models.models import ProductDB

PRODUCT = {
    'name': 'test',
}


async def create_products(override_get_async_session, product_type, count: int = 0):
    """Create a list of products."""
    for _ in range(count):
        await create_product(override_get_async_session, product_type)


async def create_product(override_get_async_session, product_type):
    """Create a product."""
    PRODUCT['product_type_id'] = product_type.id
    product = ProductDB(**PRODUCT)
    override_get_async_session.add(product)
    await override_get_async_session.commit()
    return product


@pytest.fixture(scope='function')
async def product_create(override_get_async_session, product_type):
    """Create a product fixtures."""
    product = await create_product(override_get_async_session, product_type)
    await create_products(override_get_async_session, product_type, 10)
    return product


@pytest.fixture(scope='function')
async def product2(override_get_async_session, product_type):
    """Create a product2 fixture."""
    return await create_product(override_get_async_session, product_type)
