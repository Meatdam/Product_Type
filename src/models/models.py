from typing import List

from sqlalchemy.orm import Mapped, relationship

from src.base.models import BaseDBModel, mc, FK


class ProductDB(BaseDBModel):
    __tablename__ = 'product'

    product_type_id: Mapped[int] = mc(FK("product_type.id", ondelete="CASCADE"))
    product_type: Mapped['ProductTypeDB'] = relationship(back_populates='product')


class ProductTypeDB(BaseDBModel):
    __tablename__ = 'product_type'
    product: Mapped[List['ProductDB']] = relationship(back_populates='product_type')
