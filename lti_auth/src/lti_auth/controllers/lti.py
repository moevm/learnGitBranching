from fastapi import Depends
from starlette import status
from starlette.requests import Request
from starlette.responses import RedirectResponse

from lti_auth.entities.domain.user import Task, TaskUser
from lti_auth.entities.web.lti import LtiRequest
from lti_auth.enums.web.lti_role import LtiRole
from lti_auth.services import js_tasks_integration_service, lti_auth_service, sessions_service, user_service
from lti_auth.services.login import login_service
from lti_auth.settings.settings import settings
from lti_auth.utils.datetime import now_utc
from lti_auth.value_objects.session_info import SessionInfo


async def v1_lti_controller(request: Request, lti_form: LtiRequest = Depends(LtiRequest.as_form)) -> RedirectResponse:  # noqa: B008
    if await _is_auth_lti_request(lti_form=lti_form, request=request):
        jwt_token = await _generate_jwt_token(lti_form=lti_form)
        await _save_user(form=lti_form, jwt_token=jwt_token)

        return await _redirect_to_task_response(task_id=lti_form.custom_task_id, jwt_token=jwt_token)
    else:
        raise lti_auth_service.LtiAuthError()


async def _generate_jwt_token(*, lti_form: LtiRequest) -> str:
    return await login_service.login_user(
        user_id=lti_form.user_id,
        pass_back_params=lti_form.pass_back_params,
        task_id=lti_form.custom_task_id,
    )


async def _is_auth_lti_request(lti_form: LtiRequest, request: Request) -> bool:
    return await lti_auth_service.is_auth_lti_request(
        oauth_consumer_key=lti_form.oauth_consumer_key,
        session_info=SessionInfo(
            timestamp=lti_form.oauth_timestamp,
            nonce=lti_form.oauth_nonce,
        ),
        lti_form=dict(await request.form()),
        request_url=str(request.url.replace(hostname=settings.nginx_host_name, port=settings.nginx_host_port)),
        request_headers=dict(request.headers),
    )


async def _save_user(*, form: LtiRequest, jwt_token: str) -> None:
    if not (user := await user_service.find_user(lms_user_id=form.user_id)):
        user = TaskUser(
            user_name=form.ext_user_username,
            person_name=form.lis_person_name_full,
            tool_consumer_instance_guid=form.tool_consumer_instance_guid,
            is_lti=True,
            params_for_pass_back=[],
            is_admin=LtiRole.instructor.value in form.roles,
            lms_user_id=form.user_id,
            tasks=[],
        )
    user.params_for_pass_back.append(form.pass_back_params)
    user.tasks.append(
        Task(
            task_id=form.custom_task_id,
            join_at=now_utc(),
            session_id=sessions_service.generate_session_id_by_jwt_token(jwt_token=jwt_token),
        ),
    )
    await user_service.upsert_task_user(user=user)


async def _redirect_to_task_response(
    *,
    task_id: str,
    jwt_token: str,
) -> RedirectResponse:
    response = RedirectResponse(
        url=js_tasks_integration_service.get_task_url(task_id=task_id),
        status_code=status.HTTP_303_SEE_OTHER,
    )
    return await _set_login_cookie(
        response=response,
        jwt_token=jwt_token,
    )


async def _set_login_cookie(
    *,
    response: RedirectResponse,
    jwt_token: str,
) -> RedirectResponse:
    login_service.set_auth_cookie(response=response, token=jwt_token)
    return response
