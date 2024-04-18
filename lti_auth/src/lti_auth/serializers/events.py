from serpyco_rs import Serializer

from lti_auth.entities.domain.events.base_stat_event import BaseStatEvent
from lti_auth.entities.web.send_stat import SendStatRequestV1

base_stat_event_serializer = Serializer(BaseStatEvent)
send_stat_request_v1_serializer = Serializer(SendStatRequestV1)
