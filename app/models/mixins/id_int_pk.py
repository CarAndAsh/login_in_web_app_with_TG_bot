from sqlalchemy import Integer, Identity
from sqlalchemy.orm import mapped_column, Mapped


class IdIntPkMixin:
    id: Mapped[int] = mapped_column(Integer, Identity(always=True), primary_key=True, autoincrement=True)