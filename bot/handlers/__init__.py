from aiogram import Router

from bot.handlers.other import other_router
from bot.handlers.user import user_router
from bot.middlewares.outer import DeleteUserMessageMiddleware

router: Router = Router()
router.include_routers(user_router, other_router)

# router.message.outer_middleware(DeleteUserMessageMiddleware())
