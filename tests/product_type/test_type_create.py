from starlette import status

from tests.base.base_test import BaseTestCase


class TestCaseProductTypeCreate(BaseTestCase):
    url = '/products/type'
    type_data = {"name": "type"}

    async def test_create_type(self):
        """Create a product type."""
        response = await self.make_post(url=self.url, data=self.type_data, status_code=status.HTTP_201_CREATED)
        assert response.get('name') == self.type_data.get('name')

    async def test_create_type_405(self):
        """Course creation test with wrong method selection (Error 405)."""
        await self.make_put(self.url, self.type_data, status_code=status.HTTP_405_METHOD_NOT_ALLOWED)

    async def test_create_type_422(self):
        """Course creation test with missing field (Error 422)."""
        await self.make_post(self.url, {}, status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)
