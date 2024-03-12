from lti_auth.services import lti_marks_service
from lti_auth.services.login.login import LoginService

login_service = LoginService(lti_marks_service=lti_marks_service)
