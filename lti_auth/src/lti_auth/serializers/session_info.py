from serpyco_rs import Serializer

from lti_auth.value_objects.session_info import SessionInfo

session_info_serializer = Serializer(SessionInfo)
session_info_list_serializer = Serializer(list[SessionInfo])
