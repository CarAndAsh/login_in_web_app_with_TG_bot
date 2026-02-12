from sqlalchemy import MetaData, String, Boolean, Integer
from sqlalchemy.orm import DeclarativeBase, declared_attr, Mapped, mapped_column

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


class User(IdIntPkMixin, Base):
    telegram_id: Mapped[int] = mapped_column(Integer, nullable=False, unique=True)
    is_bot: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    first_name: Mapped[str] = mapped_column(String(length=50), nullable=True)
    last_name: Mapped[str] = mapped_column(String(length=100), nullable=True)
    username: Mapped[str] = mapped_column(String(length=50), unique=True)
    language_code: Mapped[str]
    hashed_password: Mapped[str] = mapped_column(String(length=1024), nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, server_default='True', nullable=False)
    is_superuser: Mapped[bool] = mapped_column(Boolean, server_default='False', nullable=False)
    is_verified: Mapped[bool] = mapped_column(Boolean, server_default='False', nullable=False)