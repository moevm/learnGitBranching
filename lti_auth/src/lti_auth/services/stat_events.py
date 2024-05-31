from lti_auth.repositories.db_repositories.stat_events import StatEventsRepositoryContract


class StatEventsService:
    def __init__(self, stat_events_repo: StatEventsRepositoryContract):
        self._stat_events_repo = stat_events_repo

    async def send_event(self, event) -> None:
        await self._stat_events_repo.insert_event(event)
