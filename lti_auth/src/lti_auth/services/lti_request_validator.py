import asyncio
import time
from functools import cached_property, cache
from typing import Any

from oauthlib.oauth1 import RequestValidator

from lti_auth.repositories.db_repositories.lti_sessions import LtiSessionsRepositoryContract
from lti_auth.value_objects.session_info import SessionInfo


class LtiRequestValidatorService(RequestValidator):
    def __init__(self, *, lti_sessions_repository: LtiSessionsRepositoryContract):
        super().__init__()

        self._lti_sessions_repository = lti_sessions_repository

    @property
    def client_key_length(self):
        return 1, 30

    @property
    def nonce_length(self):
        return 1, 40  # len(nonce_from_moodle) = 32. default_return = (20, 30)

    @property
    def enforce_ssl(self):
        return False

    @property
    def dummy_client(self):
        return "dummy_client"

    def get_client_secret(self, oauth_consumer_key: str, request: Any) -> str:
        return self.client_secret(oauth_consumer_key=oauth_consumer_key)

    @cache
    def client_secret(self, oauth_consumer_key: str) -> str:
        return asyncio.run(self._lti_sessions_repository.get_user_secret(oauth_consumer_key=oauth_consumer_key))

    def validate_client_key(self, oauth_consumer_key, request):
        return self.is_oauth_consumer_key_exists(oauth_consumer_key=oauth_consumer_key)

    @cache
    def is_oauth_consumer_key_exists(self, oauth_consumer_key: str) -> bool:
        return asyncio.run(
            self._lti_sessions_repository.is_oauth_consumer_key_exists(
                oauth_consumer_key=oauth_consumer_key,
            ),
        )

    def validate_timestamp_and_nonce(
        self,
        oauth_consumer_key,
        timestamp,
        nonce,
        request,
        request_token=None,
        access_token=None,
    ):
        start = time.time()
        loop = asyncio.get_event_loop()

        session_info = SessionInfo(timestamp=int(timestamp), nonce=nonce)
        is_info_exists_coro = self._lti_sessions_repository.is_session_info_exists(
            oauth_consumer_key=oauth_consumer_key,
            session_info=session_info,
        )
        # return not loop.run_until_complete(is_info_exists_coro)
        loop.run_until_complete(is_info_exists_coro)
        print(f'timestamp {time.time() - start}')
        return True
