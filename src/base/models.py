from sqlalchemy import ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

FK = ForeignKey
mc = mapped_column


class BaseDBModel(DeclarativeBase):
    """Base class for database"""

    id: Mapped[int] = mc(primary_key=True)
    name: Mapped[str] = mc(nullable=False, unique=False)
