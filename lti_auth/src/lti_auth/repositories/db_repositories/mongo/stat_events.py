from motor.core import AgnosticCollection

from lti_auth.entities.domain.events.base_stat_event import BaseStatEvent
from lti_auth.repositories.db_repositories.stat_events import StatEventsRepositoryContract
from lti_auth.serializers.events import base_stat_event_serializer


class StatEventsMongoRepository(StatEventsRepositoryContract):
    def __init__(self, stat_events_collection: AgnosticCollection):
        self._stat_events_collection = stat_events_collection

    async def insert_event(self, event: BaseStatEvent) -> None:
        raw_value = base_stat_event_serializer.dump(event)

        await self._stat_events_collection.insert_one(raw_value)
