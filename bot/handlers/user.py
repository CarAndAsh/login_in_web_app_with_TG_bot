from logging import getLogger

from aiogram import F, Router
from aiogram.filters import CommandStart, StateFilter, Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.types import Message, ReplyKeyboardRemove, CallbackQuery
from aiohttp import request, web_exceptions

from bot.bot_core import FSMAuthUser
from bot.bot_core.config import settings
from bot.keyboards.keyboards import reply_keyboard, link_keyboard, confirm_account_kb
from bot.lexicon.lexicon_ru import FINAL_BOT_MESSAGE

user_router: Router = Router()

log = getLogger(__name__)


@user_router.message(Command('reset_fsm'))
async def reset_fsm(msg: Message, state: FSMContext) -> None:
    await msg.delete()
    editable_msg = await state.get_value('edit_msg_id')
    await state.set_state(default_state)
    if editable_msg:
        await editable_msg.edit_text('Начнем сначала')
    else:
        await msg.answer('Начнем сначала', reply_markup=ReplyKeyboardRemove())



@user_router.message(CommandStart(), StateFilter(default_state))
async def startup(msg: Message, state: FSMContext) -> Message:
    await msg.delete()
    await state.set_state(FSMAuthUser.check_user)
    return await msg.answer('Для входа на сайт нажмите кнопку ниже 👇',reply_markup=reply_keyboard)


@user_router.callback_query(F.data == 'check_user', FSMAuthUser.check_user)
async def get_user_data(cbq: CallbackQuery, state: FSMContext) -> Message:
    user_data = cbq.from_user.model_dump(
        include={'id', 'is_bot', 'first_name', 'last_name', 'username', 'language_code'}
    )
    user_tg_id: int = user_data.pop('id')
    user_data['telegram_id'] = user_tg_id

    async with request('POST', settings.check_user_email, json=user_tg_id) as req:
        try:
            user_email = await req.json()
        except web_exceptions.HTTPException:
           return await cbq.message.edit_text('Ошибка связи')

    if user_email:
        await state.set_data({'username':user_email}) # fastapi-users needs e-mail as username
        await state.set_state(FSMAuthUser.login_password_fill)
        await cbq.message.edit_text(
            f'Ваш e-mail, зарегистрированный в системе - {user_email}. Введите пароль для входа',
        )
    else:
        await state.set_data(user_data)
        await state.set_state(FSMAuthUser.email_fill)
        await cbq.message.edit_text(
            'Ваш e-mail, не указан в системе, для регистрации укажите его в поле ввода',
        )
    await state.update_data({'edit_msg_id':cbq.message})


@user_router.message(FSMAuthUser.email_fill)
async def get_users_email(msg:Message, state: FSMContext):
    await state.update_data({'email':msg.text})
    await msg.delete()
    editable_msg = await state.get_value('edit_msg_id')
    email = await state.get_value('email')
    async with request('POST', settings.check_user_by_email, json=email) as req:
        try:
            response = await req.json()
        except web_exceptions.HTTPException:
           return editable_msg.edit_text('Ошибка связи')
    if email == response['email'] and response['telegram_id'] is None:
        await editable_msg.edit_text(
            'Аккаунт с таким e-mail уже существует. Если он ваш, добавить к нему данные из Telegram?',
        reply_markup=confirm_account_kb)
    elif email == response['email'] and response['telegram_id'] != msg.from_user.id:
        await editable_msg.edit_text('Вы ввели e-mail существующего аккаунта, повторите ввод')
    else:
        await editable_msg.edit_text('e-mail принят, теперь введите пароль')
        await state.set_state(FSMAuthUser.register_password_fill)




@user_router.message(FSMAuthUser.password_fill)
async def get_users_password(msg:Message, state: FSMContext):
@user_router.message(FSMAuthUser.register_password_fill)
async def get_users_register_password(msg:Message, state: FSMContext):
    user_data = await state.get_data()
    user_data['password'] = msg.text
    await msg.delete()
    editable_msg: Message = user_data.pop('edit_msg_id')
    name = msg.from_user.first_name
    async with request('POST', settings.user_register, data=user_data) as req:
        url = req.url.human_repr().removesuffix(req.url.path)
        resp_token = await req.text()
    if resp_token:
        keyboard = link_keyboard(url=url+f'/tg_redirect/{resp_token.strip('"')}/{user_data.get("email")}')
        await editable_msg.edit_text(FINAL_BOT_MESSAGE['register'].format(name=name), reply_markup=keyboard)
        await state.clear()
    else:
        await editable_msg.edit_text('Неверно указан пароль, повторите ввод пароля')


@user_router.message(FSMAuthUser.login_password_fill)
async def get_users_login_password(msg:Message, state: FSMContext):
    user_data = await state.get_data()
    user_data['password'] = msg.text
    await msg.delete()
    editable_msg: Message = user_data.pop('edit_msg_id')
    name = msg.from_user.first_name
    async with request('POST', settings.login_user, data=user_data) as req:
        url = req.url.human_repr().removesuffix(req.url.path)
        resp_token = req.cookies.get('user-auth').value
    if resp_token:
        keyboard = link_keyboard(url=url+f'/tg_redirect/{resp_token.strip('"')}/{user_data.get("username")}')
        await editable_msg.edit_text(FINAL_BOT_MESSAGE['login'].format(name=name), reply_markup=keyboard)
        await state.clear()
    else:
        await editable_msg.edit_text('Неверно указан пароль, повторите ввод пароля')
