from pydantic import BaseModel


class UserSchema(BaseModel):
    is_bot: bool
    first_name: str
    last_name: str
    username: str
    language_code: str

class ReadUserSchema(UserSchema):
    id:int

class CreateUserSchema(UserSchema):
    pass

class DeleteUserSchema(ReadUserSchema):
    pass

