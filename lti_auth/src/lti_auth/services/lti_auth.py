from typing import Any

from fastapi import HTTPException
from lti import ToolProvider  # type: ignore[import-untyped]

from lti_auth.repositories.db_repositories.lti_sessions import LtiSessionsRepositoryContract
from lti_auth.services.lti_request_validator import LtiRequestValidatorService
from lti_auth.value_objects.session_info import SessionInfo


class LtiAuthService:
    def __init__(
        self,
        *,
        lti_sessions_repository: LtiSessionsRepositoryContract,
        lti_request_validator_service: LtiRequestValidatorService,
    ):
        self._lti_sessions_repository = lti_sessions_repository
        self._lti_request_validator_service = lti_request_validator_service

    async def is_auth_lti_request(
        self,
        *,
        oauth_consumer_key: str,
        session_info: SessionInfo,
        lti_form: dict[str, Any],
        request_url: str,
        request_headers: dict[str, str],
    ) -> bool:
        provider = ToolProvider.from_unpacked_request(
            secret=await self.get_oauth_secret_key(oauth_consumer_key),
            params=lti_form,
            url=request_url,
            headers=request_headers,
        )

        is_valid_request = provider.is_valid_request(self._lti_request_validator_service)
        if is_valid_request:
            await self.add_session_info(
                oauth_consumer_key=oauth_consumer_key,
                session_info=session_info,
            )

        return is_valid_request

    async def get_oauth_secret_key(self, oauth_consumer_key: str) -> str:
        return await self._lti_sessions_repository.get_user_secret(oauth_consumer_key=oauth_consumer_key)

    async def is_oauth_consumer_key_exists(self, oauth_consumer_key: str) -> bool:
        return await self._lti_sessions_repository.is_oauth_consumer_key_exists(
            oauth_consumer_key=oauth_consumer_key,
        )

    async def is_session_info_exists(self, oauth_consumer_key: str, *, session_info: SessionInfo) -> bool:
        return await self._lti_sessions_repository.is_session_info_exists(
            oauth_consumer_key=oauth_consumer_key,
            session_info=session_info,
        )

    async def add_session_info(self, oauth_consumer_key: str, *, session_info: SessionInfo) -> None:
        await self._lti_sessions_repository.add_session_info(
            oauth_consumer_key=oauth_consumer_key,
            session_info=session_info,
        )

    class LtiAuthError(HTTPException):
        def __init__(self):
            super().__init__(status_code=401, detail="LTI auth error")
