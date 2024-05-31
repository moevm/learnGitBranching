from typing import Any

from motor.core import AgnosticCollection

from lti_auth.repositories.db_repositories.lti_sessions import LtiSessionsRepositoryContract
from lti_auth.serializers.session_info import session_info_list_serializer, session_info_serializer
from lti_auth.value_objects.session_info import SessionInfo


class LtiSessionsMongoRepository(LtiSessionsRepositoryContract):
    def __init__(self, *, consumers_collection: AgnosticCollection):
        self._consumers_collection = consumers_collection

    async def get_user_secret(self, *, oauth_consumer_key: str) -> str:
        consumer = await self._get_consumer(oauth_consumer_key=oauth_consumer_key)
        consumer = consumer if consumer is not None else {}

        secret = consumer.get("oauth_consumer_secret", None)
        if secret is None:
            raise self.UnknownOauthConsumerKeyError
        return secret

    async def add_session_info(self, oauth_consumer_key: str, *, session_info: SessionInfo) -> None:
        update_query = {"$push": {"sessions": session_info_serializer.dump(session_info)}}

        consumer = await self._consumers_collection.update_one(
            filter={"oauth_consumer_key": oauth_consumer_key},
            update=update_query,
        )

        if consumer is None:
            raise self.UnknownOauthConsumerKeyError

    async def is_oauth_consumer_key_exists(self, oauth_consumer_key: str) -> bool:
        consumer = await self._get_consumer(oauth_consumer_key=oauth_consumer_key)

        return consumer is not None

    async def is_session_info_exists(self, oauth_consumer_key: str, *, session_info: SessionInfo) -> bool:
        consumer = await self._get_consumer(oauth_consumer_key=oauth_consumer_key)
        if consumer is None:
            raise self.UnknownOauthConsumerKeyError

        sessions = session_info_list_serializer.load(consumer.get("sessions", []))
        return session_info in sessions

    async def _get_consumer(self, oauth_consumer_key: str) -> dict[str, Any] | None:
        get_value = {"oauth_consumer_key": oauth_consumer_key}
        return await self._consumers_collection.find_one(filter=get_value)
