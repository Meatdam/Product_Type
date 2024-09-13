from pydantic import BaseModel

from src.product.schemas import ProductNameSchema


class TypeProductBaseSchema(BaseModel):
    """Type product base schema."""
    name: str


class CreateTypeProductSchema(TypeProductBaseSchema):
    """Create type product schema."""


class TypeProductSchema(TypeProductBaseSchema):
    """Type product detail schema."""
    id: int


class ProductTypeDetailSchema(BaseModel):
    """Scheme for detailed description of product type with reference to products."""
    id: int
    name: str
    product: list[ProductNameSchema] | None = None
