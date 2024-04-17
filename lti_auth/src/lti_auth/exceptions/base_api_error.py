import logging
from dataclasses import dataclass

logger = logging.getLogger(__name__)


@dataclass(slots=True, kw_only=True)
class Error:
    key: str | None = None
    """Название поля"""
    code: str | None = None
    """Код ошибки"""
    message: str | None = None
    """Сообщение об ошибке"""


@dataclass(slots=True, kw_only=True)
class BadRequestData:
    errors: list[Error]
    """Список ошибок"""


class BaseApiError(Exception):
    """Базовая API ошибка, чтобы было удобно отлавливать и обрабатывать"""

    def __init__(self, errors: list[Error]) -> None:
        super().__init__()
        self.errors = errors
