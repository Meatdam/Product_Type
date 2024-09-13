from starlette import status

from tests.base.base_test import BaseTestCase
from tests.conftest import get_random_value


class TestCaseProductDetail(BaseTestCase):
    """Test Product get."""
    url = '/products'

    async def test_get_product(self, product_create):
        """Test get product."""
        url = f'{self.url}/{product_create.id}/'
        response = await self.make_get(url)
        assert response.get('id') == product_create.id

    async def test_get_product_404(self):
        """Test for getting a product with a non-existent id (error 404)."""
        product_id = get_random_value()
        url = f'{self.url}/{product_id}/'
        await self.make_get(url, status_code=status.HTTP_404_NOT_FOUND)

    async def test_get_product_405(self, product_create):
        """Test for receiving a product with the wrong method selected (Error 405)."""
        url = f'{self.url}/{product_create.id}'
        await self.make_post(url, None, status_code=status.HTTP_405_METHOD_NOT_ALLOWED)

    async def test_get_product_422(self, product_create):
        """Test for getting a course with a logical error in the request (error 422)."""
        url = f'{self.url}/{product_create}'
        await self.make_get(url, status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)
