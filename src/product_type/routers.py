from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from src.base.responses import ResponseSchema
from src.config.session import get_async_session
from src.product_type.session import ProductTypeSessions
from src.product_type.shemas import CreateTypeProductSchema, ProductTypeDetailSchema

product_type_router = APIRouter()

responses = ResponseSchema()


@product_type_router.post(
    '/',
    response_model=CreateTypeProductSchema,
    responses=responses(CreateTypeProductSchema, status.HTTP_201_CREATED, [status.HTTP_409_CONFLICT]),
    status_code=status.HTTP_201_CREATED,
    description='Prodict type create',
)
async def create_product_type(
        type_product_data: CreateTypeProductSchema,
        session: AsyncSession = Depends(get_async_session),
) -> CreateTypeProductSchema:
    """Create a product type"""
    return await ProductTypeSessions(session).create_product_type(type_product_data)


@product_type_router.get(
    '/{type_id}',
    response_model=ProductTypeDetailSchema,
    responses=responses(ProductTypeDetailSchema, statuses=[status.HTTP_404_NOT_FOUND]),
    description='Product type detail',
)
async def product_type_detail(
        type_id: int,
        session: AsyncSession = Depends(get_async_session),
) -> ProductTypeDetailSchema:
    """Product type detail"""
    product_type = await ProductTypeSessions(session).get_product_type_by_id(type_id)
    if product_type:
        return product_type
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Product type not found')
