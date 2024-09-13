from typing import Annotated
from fastapi_pagination.ext.sqlalchemy import paginate

from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy import Select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from src.base.paginate_config import PaginatePage
from src.base.responses import ResponseSchema
from src.config.session import get_async_session
from src.product.schemas import CreateProductSchema, ProductListSchema, ProductDetailSchema
from src.product.session import ProductSessions

product_router = APIRouter()

responses = ResponseSchema()


@product_router.post(
    '/',
    response_model=CreateProductSchema,
    responses=responses(CreateProductSchema, status.HTTP_201_CREATED, [status.HTTP_409_CONFLICT]),
    status_code=status.HTTP_201_CREATED,
    description='Prodict create',
)
async def create_product(
        product_data: CreateProductSchema,
        session: AsyncSession = Depends(get_async_session),
) -> CreateProductSchema:
    """Create a product."""
    return await ProductSessions(session).create_product(product_data)


@product_router.get(
    '/',
    response_model=PaginatePage[ProductListSchema],
    responses=responses(PaginatePage[ProductListSchema]),
    description='Product list',
)
async def product_list(
        search: Annotated[str | None, Query(description='Search field')] = None,
        session: AsyncSession = Depends(get_async_session)
) -> PaginatePage[ProductListSchema]:
    """List of products."""
    products: Select = await ProductSessions(session).get_products_list(search)
    return await paginate(session, products)


@product_router.get(
    '/{product_id}/',
    response_model=ProductDetailSchema,
    responses=responses(ProductDetailSchema, statuses=[status.HTTP_404_NOT_FOUND]),
    description='Product detail',
)
async def product_detail(
        product_id: int,
        session: AsyncSession = Depends(get_async_session),
) -> ProductDetailSchema:
    """Product detail."""
    product = await ProductSessions(session).get_product_by_id(product_id)
    if product:
        return product
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Product not found')
