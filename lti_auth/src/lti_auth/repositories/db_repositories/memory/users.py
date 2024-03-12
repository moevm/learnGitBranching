from lti_auth.entities.domain.user import BaseUser, TaskUser
from lti_auth.repositories.db_repositories.users import UsersRepositoryContract

users: dict[str, BaseUser | TaskUser] = {}


class MemoryUsersRepository(UsersRepositoryContract):
    async def upsert_user(self, user: BaseUser) -> None:
        task_id = getattr(users.get(user.id), "task_id", None)
        task_id = getattr(user, "task_id", task_id)

        if task_id:
            user = TaskUser(**user.serializer.dump(user), task_id=task_id)

        users[user.id] = user

    async def upsert_task_user(self, user: TaskUser) -> None:
        users[user.id] = user

    async def is_exists_task_user(self, *, lms_user_id: str, task_id: str) -> bool:
        for user in users.values():
            if user.lms_user_id == lms_user_id and getattr(user, "task_id", None) == task_id:
                return True
        return False
