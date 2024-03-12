from dataclasses import dataclass

from lti import OutcomeResponse, ToolProvider  # type: ignore[import-untyped]

from lti_auth.entities.domain.pass_back_params import LtiPassBackParams
from lti_auth.serializers.pass_back_params import pass_back_params_serializer
from lti_auth.services.lti_auth import LtiAuthService


@dataclass
class LtiMarksService:
    lti_auth_service: LtiAuthService

    async def get_score(self, pass_back_params: LtiPassBackParams) -> float | None:
        provider = await self._get_provider(pass_back_params=pass_back_params)

        res: OutcomeResponse = provider.post_read_result()
        return float(res.score) if res.score else None

    async def _get_provider(self, pass_back_params: LtiPassBackParams):
        consumer_key = pass_back_params.oauth_consumer_key
        consumer_secret = await self.lti_auth_service.get_oauth_secret_key(oauth_consumer_key=consumer_key)
        return ToolProvider.from_unpacked_request(
            secret=consumer_secret,
            params=pass_back_params_serializer.dump(pass_back_params),
            url=None,
            headers=None,
        )

    async def send_score(self, pass_back_params: LtiPassBackParams, score: float) -> None:
        provider = await self._get_provider(pass_back_params=pass_back_params)
        provider.post_replace_result(score=score)
