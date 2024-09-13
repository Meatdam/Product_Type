from starlette import status

from tests.base.base_test import BaseTestCase
from tests.conftest import get_random_value


class TestCaseTypeProductGet(BaseTestCase):
    url = '/products/type'

    async def test_get_type(self, product_type):
        """Test get_type."""
        url = f'{self.url}/{product_type.id}'
        response = await self.make_get(url)
        assert response.get('id') == product_type.id

    async def test_get_type_404(self):
        """Test get_type_404."""
        type_id = get_random_value()
        url = f'{self.url}/{type_id}/'
        await self.make_get(url, status_code=status.HTTP_404_NOT_FOUND)

    async def test_get_type_405(self, product_type):
        """Test get_type_405."""
        url = f'{self.url}/{product_type.id}'
        await self.make_post(url, None, status_code=status.HTTP_405_METHOD_NOT_ALLOWED)

    async def test_get_type_422(self, product_type):
        """Test get_type_422."""
        url = f'{self.url}/{product_type}'
        await self.make_get(url, status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)
