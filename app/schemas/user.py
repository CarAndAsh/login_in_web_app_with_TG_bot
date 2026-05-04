from fastapi_users.schemas import BaseUser, BaseUserCreate, BaseUserUpdate
from pydantic import EmailStr, BaseModel, ConfigDict


# TODO something for hide 'id' field

class TelegramUserSchema(BaseModel):
    telegram_id: int | None
    is_bot: bool = False
    first_name: str | None
    last_name: str | None
    username: str
    language_code: str | None


class UserSchema(BaseUser[int], TelegramUserSchema):
    email: EmailStr | None = None


class PartialUpdateUserSchema(UserSchema, BaseUserUpdate, TelegramUserSchema):
    is_bot: bool | None = None
    username: str | None = None
    language_code: str | None = None


class CreateUserSchema(UserSchema, BaseUserCreate, TelegramUserSchema):
    id : None = None
    email: EmailStr | None = None
    telegram_id: int | None = None
    language_code: str | None = None
