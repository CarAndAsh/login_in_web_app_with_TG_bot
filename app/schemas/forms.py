from pydantic import BaseModel
from starlette_wtf import StarletteForm
from wtforms import (StringField, SubmitField, PasswordField, EmailField, BooleanField)


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


class UserForm(StarletteForm):
    first_name = StringField('Имя')
    last_name = StringField('Фамилия')
    telegram_id = StringField('телеграм ID')
    email = EmailField('E-mail')
    username = StringField('Никнейм')
    password = PasswordField('Пароль')
    confirm_password = PasswordField('Подтверждение')
    is_verified = BooleanField('Подтвержден')
    submit = SubmitField('Сохранить')


class LoginDataForm(BaseModel):
    email: str
    password: str


class RegisterDataForm(BaseModel):
    first_name: str
    last_name: str
    username: str
    email: str
    password: str
    confirm_password: str
