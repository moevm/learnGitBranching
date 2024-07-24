from lti_auth.controllers.lti import v1_lti_controller
from lti_auth.controllers.send_score import v1_send_score_controller
from lti_auth.controllers.send_stat import v1_send_stat_controller
from lti_auth.enums.web.request_method import RequestMethod
from lti_auth.web.handlers.base_handlers import Handler

app_handlers = [
    Handler(method=RequestMethod.post, path="/public/v1/lti/", controller=v1_lti_controller),
    Handler(method=RequestMethod.post, path="/v1/send-score/", controller=v1_send_score_controller),
    Handler(method=RequestMethod.post, path="/v1/send-stat/", controller=v1_send_stat_controller),
]
