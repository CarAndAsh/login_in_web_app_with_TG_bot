from sqlalchemy import MetaData
from sqlalchemy.orm import DeclarativeBase, declared_attr, Mapped, mapped_column
from fastapi_users.db import SQLAlchemyBaseUserTable

from app.core.app_config import settings
from app.models.mixins.id_int_pk import IdIntPkMixin


class Base(DeclarativeBase):
    __abstract__ = True
    metadata = MetaData(naming_convention=settings.db.naming_convention)

    @declared_attr.directive
    def __tablename__(cls) -> str:
        return f'{cls.__name__.lower()}s'

    def to_dict(self):
        return {k:v for k, v in self.__dict__.items() if not k.startswith('_')}


class User(IdIntPkMixin, Base, SQLAlchemyBaseUserTable[int]):
    telegram_id: Mapped[int]
    is_bot: Mapped[bool]
    first_name: Mapped[str] = mapped_column(nullable=True)
    last_name: Mapped[str] = mapped_column(nullable=True)
    username: Mapped[str] = mapped_column(unique=True)
    language_code: Mapped[str] = mapped_column()