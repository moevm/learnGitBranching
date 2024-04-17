from fastapi import status
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import JSONResponse

from lti_auth.exceptions.base_api_error import BadRequestData, BaseApiError
from lti_auth.serializers.bad_request_data import bad_request_data_serializer


class HandleErrorsMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint):
        try:
            return await call_next(request)
        except BaseApiError as exc:
            error = BadRequestData(errors=exc.errors)
            content = bad_request_data_serializer.dump(error)
            return JSONResponse(
                content=content,
                status_code=status.HTTP_400_BAD_REQUEST,
            )
