from pydantic import ConfigDict, BaseModel


class BaseUserSchema(BaseModel):
    telegram_id: int
    is_bot: bool
    first_name: str | None
    last_name: str | None
    username: str
    language_code: str
    is_active: bool = True
    is_superuser: bool = False
    is_verified: bool = False

    model_config = ConfigDict(from_attributes=True)


class UserSchema(BaseUserSchema):
    id: int


class UpdateUserSchema(BaseUserSchema):
    pass


class PartialUpdateUserSchema(BaseModel):
    telegram_id: int | None = None
    is_bot: bool | None = None
    first_name: str | None = None
    last_name: str | None = None
    username: str | None = None
    language_code: str | None = None
    is_active: bool = True
    is_verified: bool = False


class CreateUserSchema(BaseUserSchema):
    pass
