from fastapi_users.schemas import BaseUser, BaseUserCreate, BaseUserUpdate
from pydantic import EmailStr, BaseModel, ConfigDict


# TODO something for hide 'id' field

class TelegramUserSchema(BaseModel):
    telegram_id: int | None = None
    is_bot: bool = False
    first_name: str | None = None
    last_name: str | None = None
    username: str
    language_code: str | None


class UserSchema(BaseUser[int], TelegramUserSchema):
    pass


class PartialUpdateUserSchema(BaseUserUpdate, UserSchema, TelegramUserSchema):
    id : None = None
    is_bot: bool | None = None
    username: str | None = None
    language_code: str | None = None


class CreateUserSchema(UserSchema, BaseUserCreate, TelegramUserSchema):
    id : None = None
    telegram_id: int | None = None
    language_code: str | None = None
