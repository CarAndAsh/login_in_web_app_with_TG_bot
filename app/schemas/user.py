from pydantic import BaseModel


class UserSchema(BaseModel):
    telegram_id: int
    is_bot: bool
    first_name: str | None
    last_name: str | None
    username: str
    language_code: str


class ReadUserSchema(UserSchema):
    id: int


class CreateUserSchema(UserSchema):
    pass


class DeleteUserSchema(ReadUserSchema):
    pass
