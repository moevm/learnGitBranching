from starlette.requests import Request

from lti_auth.entities.web.send_mark import SendMarkRequestV1
from lti_auth.services import lti_marks_service
from lti_auth.services.login import login_service
from lti_auth.settings.settings import settings


async def v1_send_score_controller(request: Request, request_data: SendMarkRequestV1) -> None:
    jwt_token = request.cookies[settings.jwt_cookie_name]
    pass_back_params = await login_service.extract_pass_back_params(jwt_token=jwt_token)

    await lti_marks_service.send_score(pass_back_params=pass_back_params, score=request_data.mark)
