import jwt
import orjson
from starlette.responses import Response

from lti_auth.entities.domain.jwt_token_payload import JwtTokenPayload
from lti_auth.entities.domain.pass_back_params import LtiPassBackParams
from lti_auth.serializers.pass_back_params import pass_back_params_serializer
from lti_auth.services import LtiMarksService
from lti_auth.settings.settings import settings


class LoginService:
    _cookie_store: dict[str | int, str] = {}

    def __init__(self, lti_marks_service: LtiMarksService):
        self._lti_marks_service = lti_marks_service

    async def login_user(self, *, user_id: str | int, pass_back_params: LtiPassBackParams, task_id: str) -> str:
        score = await self._lti_marks_service.get_score(pass_back_params=pass_back_params)
        success = score == 1
        data = JwtTokenPayload(
            user_id=str(user_id),
            task_id=task_id,
            pass_back_params=pass_back_params,
            is_success=success,
        )
        token = self._encode_jwt_token(token_data=data)

        self._cookie_store[user_id] = token

        return token

    @staticmethod
    def _encode_jwt_token(token_data: JwtTokenPayload) -> str:
        pass_back_params_data = pass_back_params_serializer.dump(token_data.pass_back_params)
        pass_back_params_json = orjson.dumps(pass_back_params_data).decode("utf-8")

        return jwt.encode(
            payload={
                settings.jwt_user_id_param_name: token_data.user_id,
                settings.jwt_task_id_param_name: token_data.task_id,
                settings.jwt_pass_back_params_param_name: pass_back_params_json,
                settings.jwt_is_success_param_name: token_data.is_success,
            },
            key=settings.jwt_secret,
            algorithm=settings.jwt_algorithm,
        )

    async def extract_pass_back_params(self, jwt_token: str) -> LtiPassBackParams:
        token_data = self.decode_jwt_token(token=jwt_token)

        return token_data.pass_back_params

    @staticmethod
    def decode_jwt_token(token: str) -> JwtTokenPayload:
        token_data = jwt.decode(token, key=settings.jwt_secret, algorithms=[settings.jwt_algorithm])
        pass_back_params_json = token_data[settings.jwt_pass_back_params_param_name]
        pass_back_params = pass_back_params_serializer.load(orjson.loads(pass_back_params_json))

        return JwtTokenPayload(
            pass_back_params=pass_back_params,
            user_id=token_data[settings.jwt_user_id_param_name],
            task_id=token_data[settings.jwt_task_id_param_name],
            is_success=token_data[settings.jwt_is_success_param_name],
        )

    @staticmethod
    def set_auth_cookie(*, response: Response, token: str) -> None:
        response.set_cookie(key=settings.jwt_cookie_name, value=token, httponly=True)
