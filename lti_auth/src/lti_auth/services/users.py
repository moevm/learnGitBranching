from lti_auth.entities.domain.user import BaseUser, TaskUser
from lti_auth.repositories.db_repositories.users import UsersRepositoryContract


class UserService:
    def __init__(self, user_repository: UsersRepositoryContract):
        self.user_repository = user_repository

    async def upsert_user(self, user: BaseUser) -> None:
        return await self.user_repository.upsert_user(user=user)

    async def upsert_task_user(self, user: TaskUser) -> None:
        return await self.user_repository.upsert_task_user(user=user)

    async def is_exists_task_user(self, *, lms_user_id: str, task_id: str) -> bool:
        return await self.user_repository.is_exists_task_user(lms_user_id=lms_user_id, task_id=task_id)

    async def find_user(self, lms_user_id: str) -> TaskUser | None:
        return await self.user_repository.find_user(lms_user_id=lms_user_id)
