from starlette import status

from tests.base.base_test import BaseTestCase
from tests.conftest import get_url_size


class TestCaseProductList(BaseTestCase):
    url = '/products'

    async def test_get_product_list(self, product_create):
        """Test get product list."""
        response = await self.make_get(self.url)
        assert len(response['items']) <= response['size']
        assert response['items'][0].get('product_type_id') is not None

    async def test_product_list_pagination(self, product_create):
        """Test for getting a list of products with pagination."""
        size = 20
        url = get_url_size(self.url, size)
        response = await self.make_get(url)
        assert len(response['items']) <= size

        size, page = 2, 3
        url = get_url_size(self.url, size, page)
        response = await self.make_get(url)
        assert len(response['items']) <= size

    async def test_product_list_search(self, product_create, product2):
        """Test for getting a list of products with search by fields."""
        url = f'{self.url}?search={product_create.name}'
        response = await self.make_get(url)
        assert response['items'][0].get('name') == f'{product_create.name}'

        url = f'{self.url}?id_search={product2.id}'
        response = await self.make_get(url)
        assert response['total'] == product2.id

    async def test_get_product_list_405(self, product_create):
        """Test for getting list of products with wrong method selection (Error 405)."""
        await self.make_delete(self.url, status_code=status.HTTP_405_METHOD_NOT_ALLOWED)

    async def test_get_product_list_422(self, product_create):
        """Test to get list of products with logical error in request (error 422)."""
        url = get_url_size(self.url, -20)
        await self.make_get(url, status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)
