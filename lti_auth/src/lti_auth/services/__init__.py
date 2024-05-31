from lti_auth.repositories.db_repositories.mongo import (
    lti_sessions_mongo_repository,
    stat_events_mongo_repository,
    users_mongo_repository,
)
from lti_auth.services.js_tasks_integration import JsTasksIntegrationService
from lti_auth.services.lti_auth import LtiAuthService
from lti_auth.services.lti_marks import LtiMarksService
from lti_auth.services.lti_request_validator import LtiRequestValidatorService
from lti_auth.services.sessions import SessionsService
from lti_auth.services.stat_events import StatEventsService
from lti_auth.services.users import UserService

lti_request_validator_service = LtiRequestValidatorService(
    lti_sessions_repository=lti_sessions_mongo_repository,
)

lti_auth_service = LtiAuthService(
    lti_sessions_repository=lti_sessions_mongo_repository,
    lti_request_validator_service=lti_request_validator_service,
)

user_service = UserService(user_repository=users_mongo_repository)

js_tasks_integration_service = JsTasksIntegrationService()

lti_marks_service = LtiMarksService(lti_auth_service=lti_auth_service)

stat_events_service = StatEventsService(stat_events_repo=stat_events_mongo_repository)

sessions_service = SessionsService()
