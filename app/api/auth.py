from fastapi import APIRouter
from fastapi_users import FastAPIUsers

from app.api.dependencies.authentication import auth_backend, get_user_manager
from app.core.app_config import settings
from app.models import User
from app.schemas.user import UserSchema, PartialUpdateUserSchema, CreateUserSchema

fastapi_users = FastAPIUsers[User, int](get_user_manager,[auth_backend])

fastapi_users_router = APIRouter(prefix=settings.api.auth ,tags=['FastAPI-Users'])

# /login, /logout
fastapi_users_router.include_router(fastapi_users.get_auth_router(auth_backend))
# /register
fastapi_users_router.include_router(fastapi_users.get_register_router(UserSchema, CreateUserSchema))
# /request-verify-token, /verify
fastapi_users_router.include_router(fastapi_users.get_verify_router(UserSchema))
# /forgot-password, /reset-password
fastapi_users_router.include_router(fastapi_users.get_reset_password_router())
# GET and PATCH me and GET, PATCH and DELETE user by id
fastapi_users_router.include_router(fastapi_users.get_users_router(UserSchema, PartialUpdateUserSchema))

current_user = fastapi_users.current_user()
current_active_user = fastapi_users.current_user(active=True)
current_superuser = fastapi_users.current_user(superuser=True)
current_active_superuser = fastapi_users.current_user(superuser=True,active=True)