from aiogram.fsm.state import StatesGroup, State

class FSMAuthUser(StatesGroup):
    check_user = State()
    email_fill = State()
    password_fill = State()
    confirm_pwd_fill = State()
    login = State()
    register = State()
