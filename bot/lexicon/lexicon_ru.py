from bot.bot_core import settings

BOT_INFO = {
    'name': 'Рег-бот',
    'short_desc': 'Бот для регистрации',
    'description': 'Данный бот собирает и передает данные пользователя в веб-приложение для автоматической регистрации или входа.'
}
BOT_BTN = {
    'get_info': 'Вход/регистрация',
    'profile': 'Переход в профиль'
}

BOT_MENU = {
    'start': 'Запуск бота',
    'info': 'Информация о боте',
    'reset_fsm': 'Сброс FSM',
}

FINAL_BOT_MESSAGE = {
    'login':'С возвращением, {name}! Перейдите в свой профиль по ссылке ниже',
    'register':'Благодарим за регистрацию, {name}. Перейдите в свой профиль по ссылке ниже'
    'FSMAuthUser:register_password_fill':'Благодарим за регистрацию, {name}. Перейдите в свой профиль по ссылке ниже',
    'FSMAuthUser:login_password_fill':'С возвращением, {name}! Перейдите в свой профиль по ссылке ниже',
}

REQUEST_URL = {
    'FSMAuthUser:register_password_fill':settings.user_register,
    'FSMAuthUser:login_password_fill':settings.login_user,
}
