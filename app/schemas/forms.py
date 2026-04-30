from pydantic import BaseModel
from starlette_wtf import StarletteForm
from wtforms import StringField, SubmitField,PasswordField, EmailField


class RegisterForm(StarletteForm):
    first_name = StringField('Имя')
    last_name = StringField('Фамилия')
    username = StringField('Никнейм')
    email = EmailField('E-mail')
    password = PasswordField('Пароль')
    confirm_password = PasswordField('Подтверждение')
    submit = SubmitField('Зарегистрироваться')


class LoginForm(StarletteForm):
    email = EmailField('E-mail')
    password = PasswordField('Пароль')
    submit = SubmitField('Войти')


class LoginDataForm(BaseModel):
    email: str
    password: str
