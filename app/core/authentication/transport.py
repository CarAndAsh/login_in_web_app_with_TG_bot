from fastapi_users.authentication import BearerTransport

from app.core.app_config import settings

bearer_transport: BearerTransport = BearerTransport(tokenUrl=settings.api.bearer_token_url)
