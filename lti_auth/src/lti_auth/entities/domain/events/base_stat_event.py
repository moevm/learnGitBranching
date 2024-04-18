from dataclasses import dataclass
from datetime import datetime

from lti_auth.enums.db.stat_event_type import StatEventType


@dataclass(slots=True, kw_only=True)
class BaseStatEvent:
    stat_event_type: StatEventType
    """Тип события"""
    session_id: str
    """Идентификатор сессии"""
    extra_data: dict
    """Дополнительные данные по событию"""
    user_ip: str
    """IP пользователя"""
    user_agent: str
    """User-Agent пользователя"""
    consumed_at: datetime
    """Когда эвент был получен"""
