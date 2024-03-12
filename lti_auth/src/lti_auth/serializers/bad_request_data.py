from serpyco_rs import Serializer

from lti_auth.exceptions.base_api_error import BadRequestData

bad_request_data_serializer = Serializer(BadRequestData)
