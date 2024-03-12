from typing import Any

from lti_auth.repositories.db_repositories.lti_sessions import LtiSessionsRepositoryContract
from lti_auth.settings.settings import settings
from lti_auth.value_objects.session_info import SessionInfo

consumers: dict[str, Any] = {settings.session_public_key: {"consumer_secret": settings.session_secret_key}}


class MemoryLtiSessionsRepository(LtiSessionsRepositoryContract):
    _sessions_key = "sessions"

    async def get_user_secret(self, oauth_consumer_key: str) -> str:
        """Получить секрет пользователя"""

        consumer = consumers.get(oauth_consumer_key, {})
        secret = consumer.get("consumer_secret", None)
        if secret is None:
            raise self.UnknownOauthConsumerKeyError
        return secret

    def _get_sessions(self, oauth_consumer_key: str) -> list[tuple[int, str]]:
        consumer: dict | None = consumers.get(oauth_consumer_key)
        if consumer is None:
            raise self.UnknownOauthConsumerKeyError

        return consumer.setdefault(self._sessions_key, [])

    async def add_session_info(self, oauth_consumer_key: str, *, session_info: SessionInfo) -> None:
        """Добавить метку времени"""

        sessions = self._get_sessions(oauth_consumer_key)
        sessions.append((session_info.timestamp, session_info.nonce))

    async def is_oauth_consumer_key_exists(self, oauth_consumer_key: str) -> bool:
        """Проверить существование ключа"""

        return oauth_consumer_key in consumers

    async def is_session_info_exists(self, oauth_consumer_key: str, *, session_info: SessionInfo) -> bool:
        """Проверить существование сессии"""

        sessions = self._get_sessions(oauth_consumer_key)
        return (session_info.timestamp, session_info.nonce) in sessions
