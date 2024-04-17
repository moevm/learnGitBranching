from abc import abstractmethod
from typing import Protocol

from lti_auth.entities.domain.user import BaseUser, TaskUser


class UsersRepositoryContract(Protocol):
    @abstractmethod
    async def upsert_user(self, user: BaseUser) -> None:
        """Создать пользователя"""

    @abstractmethod
    async def upsert_task_user(self, user: TaskUser) -> None:
        """Сохраняем пользователя, пришедшего по конкретной задаче"""

    @abstractmethod
    async def is_exists_task_user(self, *, lms_user_id: str, task_id: str) -> bool:
        """Проверка существования пользователя по задаче"""
