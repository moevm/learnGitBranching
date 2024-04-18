from abc import abstractmethod
from typing import Protocol

from lti_auth.entities.domain.events.base_stat_event import BaseStatEvent


class StatEventsRepositoryContract(Protocol):
    @abstractmethod
    async def insert_event(self, event: BaseStatEvent) -> None:
        """Создать пользователя"""
