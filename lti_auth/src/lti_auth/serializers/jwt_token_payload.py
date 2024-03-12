from serpyco_rs import Serializer

from lti_auth.entities.domain.jwt_token_payload import JwtTokenPayload

jwt_token_payload_serializer = Serializer(JwtTokenPayload)
