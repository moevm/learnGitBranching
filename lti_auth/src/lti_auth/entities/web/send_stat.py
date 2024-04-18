from dataclasses import dataclass
from typing import Any

from lti_auth.enums.db.stat_event_type import StatEventType


@dataclass(slots=True, kw_only=True)
class SendStatRequestV1:
    """Запрос на отправку статистики"""

    stat_event_type: StatEventType
    """Тип события"""
    jwt_token: str
    """JWT токен"""
    extra_data: dict[str, Any]
    """Дополнительные данные по событию"""
    user_ip: str
    """IP пользователя"""
    user_agent: str
    """User-Agent пользователя"""
