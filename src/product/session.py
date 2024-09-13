from sqlalchemy import insert, Select, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from sqlalchemy.exc import IntegrityError

from src.base.utils import handle_error
from src.models.models import ProductDB
from src.product.schemas import CreateProductSchema, ProductDetailSchema


class ProductSessions:

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create_product(self, data: CreateProductSchema):
        """Create product in the database."""
        async with self.session.begin():
            product = data.model_dump()
            try:
                query = insert(ProductDB).values(**product).returning(ProductDB)
                return await self.session.scalar(query)
            except IntegrityError as err:
                return handle_error(err)

    async def get_products_list(self, value: str | None) -> Select:
        """Returns all products."""
        async with self.session.begin():
            query = select(ProductDB)
            if value:
                query = query.filter(
                    ProductDB.name.ilike(f'%{value}%'),
                ).distinct()
            return query

    async def get_product_by_id(self, product_id: int) -> ProductDetailSchema:
        """Returns product by id."""
        async with self.session.begin():
            query = select(ProductDB).filter_by(id=product_id).options(selectinload(ProductDB.product_type))
            result = await self.session.execute(query)
            product = result.first()
            result, = product or (None,)
            return result
