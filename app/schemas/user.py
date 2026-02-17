from fastapi_users.schemas import BaseUser, BaseUserCreate, BaseUserUpdate

# TODO something for hide 'id' field

class BaseUserSchema(BaseUser[int]):
    telegram_id: int | None
    is_bot: bool
    first_name: str | None
    last_name: str | None
    username: str
    language_code: str


class UserSchema(BaseUserSchema):
    pass


class PartialUpdateUserSchema(BaseUserSchema, BaseUserUpdate):
    telegram_id: int | None = None
    is_bot: bool | None = None
    first_name: str | None = None
    last_name: str | None = None
    username: str | None = None
    language_code: str | None = None


class CreateUserSchema(BaseUserSchema, BaseUserCreate):
    pass
