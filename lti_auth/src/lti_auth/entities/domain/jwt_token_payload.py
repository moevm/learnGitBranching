from dataclasses import dataclass

from lti_auth.entities.domain.pass_back_params import LtiPassBackParams


@dataclass(slots=True, kw_only=True)
class JwtTokenPayload:
    """Payload токена"""

    user_id: str
    """Идентификатор пользователя"""
    task_id: str
    """Идентификатор задания"""
    given_name: str
    """Имя пользователя из LMS"""
    family_name: str
    """Фамилия пользователя из LMS"""
    full_name: str
    """Полное имя пользователя из LMS"""
    pass_back_params: LtiPassBackParams
    """Параметры для передачи (json)"""
    is_success: bool
    """Было ли успешно"""
