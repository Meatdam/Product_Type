from sqlalchemy import insert, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.base.utils import handle_error
from src.models.models import ProductTypeDB
from src.product_type.schemas import CreateTypeProductSchema, ProductTypeDetailSchema


class ProductTypeSessions:

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create_product_type(self, data: CreateTypeProductSchema):
        """Create product type"""
        async with self.session.begin():
            product_type = data.model_dump()
            try:
                query = insert(ProductTypeDB).values(**product_type).returning(ProductTypeDB)
                return await self.session.scalar(query)
            except IntegrityError as err:
                print(f'Посмотри {err}')
                return handle_error(err)

    async def get_product_type_by_id(self, type_id: int) -> ProductTypeDetailSchema:
        """Get product type by id"""
        async with self.session.begin():
            query = select(ProductTypeDB).filter_by(id=type_id).options(selectinload(ProductTypeDB.product))
            result = await self.session.execute(query)
            product_type = result.first()
            result, = product_type or (None,)
            return result
