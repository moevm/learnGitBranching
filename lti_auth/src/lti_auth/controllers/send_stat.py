from lti_auth.entities.domain.events.base_stat_event import BaseStatEvent
from lti_auth.entities.web.send_stat import SendStatRequestV1
from lti_auth.services import sessions_service, stat_events_service
from lti_auth.utils.datetime import now_utc


async def v1_send_stat_controller(request: SendStatRequestV1) -> None:
    await stat_events_service.send_event(
        BaseStatEvent(
            stat_event_type=request.stat_event_type,
            session_id=sessions_service.generate_session_id_by_jwt_token(request.jwt_token),
            extra_data=request.extra_data,
            user_ip=request.user_ip,
            user_agent=request.user_agent,
            consumed_at=now_utc(),
        ),
    )
