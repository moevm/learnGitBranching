from typing import Any

from motor.core import AgnosticCollection

from lti_auth.entities.domain.user import BaseUser, TaskUser
from lti_auth.repositories.db_repositories.users import UsersRepositoryContract
from lti_auth.serializers.user import task_user_serializer


class UsersMongoRepository(UsersRepositoryContract):
    def __init__(self, *, users_collection: AgnosticCollection):
        self.users_collection = users_collection

    async def upsert_user(self, user: BaseUser) -> None:
        is_user_exists = await self.is_user_exists(lms_user_id=user.lms_user_id)

        if is_user_exists:
            await self.update_user(user=user)
        else:
            await self.insert_user(user=user)

    async def is_exists_task_user(self, *, lms_user_id: str, task_id: str) -> bool:
        task_filter = {"task_id": task_id}
        return await self.is_user_exists(lms_user_id=lms_user_id, extend_filters=task_filter)

    async def upsert_task_user(self, user: TaskUser) -> None:
        task_filter = {"task_id": user.task_id}
        if await self.is_user_exists(lms_user_id=user.lms_user_id, extend_filters=task_filter):
            await self.update_user(user=user, extend_filters=task_filter)
        else:
            await self.insert_user(user=user)

    async def find_user(self, lms_user_id: str) -> TaskUser | None:
        return await self.find_user_by_lms_user_id(lms_user_id=lms_user_id)

    # ДОП. ФУНКЦИИ
    async def insert_user(self, user: BaseUser) -> None:
        user_data = user.serializer.dump(user)
        await self.users_collection.insert_one(document=user_data)

    async def insert_task_user(self, user: BaseUser) -> None:
        user_data = user.serializer.dump(user)
        await self.users_collection.insert_one(document=user_data)

    async def update_user(self, user: BaseUser, *, extend_filters: dict[str, Any] | None = None) -> None:
        user_data = user.serializer.dump(user)
        filter_query = {"lms_user_id": user.lms_user_id}
        if extend_filters:
            filter_query.update(extend_filters)

        await self.users_collection.find_one_and_replace(filter=filter_query, replacement=user_data)

    async def is_user_exists(self, lms_user_id: str, *, extend_filters: dict[str, Any] | None = None) -> bool:
        filter_query = {"lms_user_id": lms_user_id}
        if extend_filters:
            filter_query.update(extend_filters)

        user = await self.find_user_by(filter_query=filter_query)

        return user is not None

    async def find_user_by(self, filter_query: dict[str, Any]) -> TaskUser | None:
        res = await self.users_collection.find_one(filter=filter_query)
        if res:
            return task_user_serializer.load(res)
        return None

    async def find_user_by_lms_user_id(self, lms_user_id: str) -> TaskUser | None:
        filter_query = {"lms_user_id": lms_user_id}
        return await self.find_user_by(filter_query=filter_query)
