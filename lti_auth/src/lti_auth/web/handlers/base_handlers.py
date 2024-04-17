from collections.abc import Awaitable, Callable
from dataclasses import dataclass

from fastapi.openapi.models import Response as FastAPIResponse
from starlette.responses import Response as StarletteResponse

from lti_auth.enums.web.request_method import RequestMethod
from lti_auth.utils.types import Dataclass


@dataclass(slots=True, kw_only=True)
class Handler:
    controller: Callable[..., Awaitable[Dataclass | None | StarletteResponse | FastAPIResponse]]
    """Контроллер для хендлера"""
    path: str
    """Путь хендлера"""
    method: RequestMethod
    """Метод хендлера"""
