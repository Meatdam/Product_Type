from pydantic import BaseModel


class ProductNameSchema(BaseModel):
    """Product name schema."""
    name: str
    id: int


class BaseProductSchema(BaseModel):
    """Base product schema."""
    id: int
    name: str
    product_type_id: int


class CreateProductSchema(BaseModel):
    """Product creation scheme."""
    name: str
    product_type_id: int


class ProductListSchema(BaseProductSchema):
    """Product list scheme."""


from src.product_type.schemas import TypeProductSchema


class ProductDetailSchema(BaseProductSchema):
    """Product detail scheme."""
    product_type: TypeProductSchema | None = None
