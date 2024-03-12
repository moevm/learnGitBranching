from dataclasses import dataclass

from serpyco_rs import Serializer

from lti_auth.entities.domain.pass_back_params import LtiPassBackParams


@dataclass(slots=True, kw_only=True)
class BaseUser:
    user_name: str
    """Логин пользователя"""
    person_name: str
    """Имя пользователя"""
    tool_consumer_instance_guid: str
    """GUID инстанса"""
    is_lti: bool
    """Является ли пользователь LTI"""
    params_for_pass_back: LtiPassBackParams
    """Параметры для передачи оценки"""
    is_admin: bool
    """Является ли пользователь администратором"""
    lms_user_id: str
    """ID пользователя в LMS (сейчас moodle)"""

    @property
    def serializer(self) -> Serializer:
        from lti_auth.serializers.user import base_user_serializer

        return base_user_serializer

    @property
    def id(self) -> str:
        return self.user_name


@dataclass(slots=True, kw_only=True)
class TaskUser(BaseUser):
    task_id: str
    """ID задачи"""

    @property
    def serializer(self) -> Serializer:
        from lti_auth.serializers.user import task_user_serializer

        return task_user_serializer
