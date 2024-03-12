from collections.abc import Awaitable, Callable

from fastapi.openapi.models import Response as FastAPIResponse
from starlette.responses import Response as StarletteResponse

from lti_auth.app import app
from lti_auth.enums.web.request_method import RequestMethod
from lti_auth.utils.types import Dataclass

controller_typing = Callable[..., Awaitable[Dataclass | None | StarletteResponse | FastAPIResponse]]


def set_handler(
    *,
    method: RequestMethod,
    path: str,
    controller: controller_typing,
) -> controller_typing:
    match method:
        case RequestMethod.get:
            app_method = app.get
        case RequestMethod.post:
            app_method = app.post
        case _:
            raise AssertionError(f"Метод {method} не поддерживается")

    return app_method(path=path)(controller)
