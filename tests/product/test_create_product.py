from starlette import status

from tests.base.base_test import BaseTestCase


class TestCaseProductTypeCreate(BaseTestCase):
    """Test case product type."""

    url = '/products'
    type_data = {"name": "type"}

    async def test_create_product(self, product_type):
        """Create a product."""
        data = self.type_data.copy()
        data['product_type_id'] = product_type.id
        response = await self.make_post(url=self.url, data=data, status_code=status.HTTP_201_CREATED)
        assert response.get('name') == self.type_data.get('name')

    async def test_create_product_405(self):
        """test create product (405) error."""
        await self.make_put(self.url, self.type_data, status_code=status.HTTP_405_METHOD_NOT_ALLOWED)

    async def test_create_product_422(self):
        """Test create product (422) error."""
        await self.make_post(self.url, {}, status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)
