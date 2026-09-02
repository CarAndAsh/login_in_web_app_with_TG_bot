from aiogram.fsm.state import StatesGroup, State

class FSMAuthUser(StatesGroup):
    check_user = State()
    email_fill = State()
    login_password_fill = State()
    register_password_fill = State()
    update_password_fill = State()
