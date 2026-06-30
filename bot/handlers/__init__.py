from aiogram import Router

from bot.handlers.other import other_router
from bot.handlers.user import user_router

router: Router = Router()
router.include_routers(user_router, other_router)

