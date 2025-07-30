import logging

from channels.db import database_sync_to_async
from channels.middleware import BaseMiddleware

from typing import Dict, Any, Optional, Union

from urllib.parse import parse_qs

from django.core.cache import cache
from django.contrib.auth.models import AnonymousUser

from rest_framework_simplejwt.tokens import AccessToken
from rest_framework_simplejwt.exceptions import TokenError

from core.models import User

logger = logging.getLogger(__name__)


class JWTAuthMiddleware(BaseMiddleware):
    CACHE_TIMEOUT = 3600 * 10  # 10 hours
    USER_CACHE_KEY_PREFIX = "websocket-user:"
    TOKEN_QUERY_PARAM = "token"

    async def __call__(self, scope: Dict[str, Any], receive, send):
        token = self._extract_token(scope)
        if token is None:
            scope["user"] = AnonymousUser()
        else:
            scope["user"] = await self.__authenticate_user(token)

        return await super().__call__(scope, receive, send)

    def _extract_token(self, scope: Dict[str, Any]) -> Optional[str]:
        try:
            # scope["query_string"] is a bytes object
            query_string = scope.get("query_string", b"").decode(errors="ignore")
            query_params = parse_qs(query_string)
            token_list = query_params.get(self.TOKEN_QUERY_PARAM, [])
            return token_list[0] if token_list else None

        except Exception as e:
            logger.error(f"Failed to decode query_string: {e}")
            return None

    @database_sync_to_async
    def __authenticate_user(self, token: str) -> Union[User, AnonymousUser]:
        try:
            validated_token = AccessToken(token)
            validated_token.check_exp()

            user_id: int = validated_token.get("user_id")
            if user_id is None:
                return AnonymousUser()

            cache_key = f"{self.USER_CACHE_KEY_PREFIX}{user_id}"
            user = cache.get(cache_key)

            if user:
                logger.debug("User loaded from cache: %s", user_id)
            else:
                user: User = User.objects.get(id=user_id)
                cache.set(cache_key, user, self.CACHE_TIMEOUT)
                logger.info("User loaded from DB and cached: %s", user_id)

            logger.info("Authenticated user ID: %s", user_id)
            return user

        except TokenError:
            logger.warning("JWT decoding failed")
            return AnonymousUser()
        except User.DoesNotExist:
            logger.warning("User not found for valid JWT")
            return AnonymousUser()
