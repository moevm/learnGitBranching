from dataclasses import dataclass


@dataclass(slots=True, kw_only=True)
class GetUserInfoRequestV1:
    user_auth_cookie: str
    """Кука авторизационной сессии (название куки хранится в settings.session_cookie_name)"""


@dataclass(kw_only=True)
class GetUserInfoResponseV1:
    lms_user_id: str
    """ID пользователя в LMS (сейчас это moodle)"""
