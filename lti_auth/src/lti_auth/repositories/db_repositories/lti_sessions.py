from typing import Protocol

from lti_auth.exceptions.base_api_error import BaseApiError
from lti_auth.value_objects.session_info import SessionInfo


class LtiSessionsRepositoryContract(Protocol):
    async def get_user_secret(self, *, oauth_consumer_key: str) -> str:
        """Получить секрет пользователя"""

    async def add_session_info(self, oauth_consumer_key: str, *, session_info: SessionInfo) -> None:
        """Добавить метку времени"""

    async def is_oauth_consumer_key_exists(self, oauth_consumer_key: str) -> bool:
        """Проверить существование ключа"""

    async def is_session_info_exists(self, oauth_consumer_key: str, *, session_info: SessionInfo) -> bool:
        """Проверить существование сессии"""

    class UnknownOauthConsumerKeyError(BaseApiError):
        """Секрет не найден"""

        def __init__(self):
            super().__init__(detail="Unknown oauth_consumer_key", status_code=400)
