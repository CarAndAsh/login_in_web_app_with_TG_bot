from pydantic import BaseModel, ConfigDict


class BaseUserSchema(BaseModel):
    telegram_id: int
    is_bot: bool
    first_name: str | None
    last_name: str | None
    username: str
    language_code: str


class UserSchema(BaseUserSchema):
    model_config = ConfigDict(from_attributes=True)
    id: int


class UpdateUserSchema(BaseUserSchema):
    pass


class PartialUpdateUserSchema(BaseUserSchema):
    telegram_id: int | None = None
    is_bot: bool | None = None
    first_name: str | None = None
    last_name: str | None = None
    username: str | None = None
    language_code: str | None = None


class CreateUserSchema(BaseUserSchema):
    pass
