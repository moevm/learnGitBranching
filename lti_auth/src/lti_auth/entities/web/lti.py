from pydantic import BaseModel

from lti_auth.entities.domain.pass_back_params import LtiPassBackParams
from lti_auth.enums.web.lti_role import LtiRole
from lti_auth.utils.dataclass_as_fast_api_form import as_form


@as_form
class LtiRequest(BaseModel):
    """Модель веб-слоя - запрос приходящий из LMS системы (сейчас moodle) по LTI протоколу"""

    oauth_version: str = ""
    oauth_nonce: str = ""
    oauth_timestamp: int = -1
    oauth_consumer_key: str = ""
    user_id: str = ""
    lis_person_sourcedid: str = ""
    roles: list[str] = []
    context_id: str = ""
    context_label: str = ""
    context_title: str = ""
    resource_link_title: str = ""
    resource_link_description: str = ""
    resource_link_id: str = ""
    context_type: str = ""
    lis_course_section_sourcedid: str = ""
    lis_result_sourcedid: str = ""
    lis_outcome_service_url: str = ""
    lis_person_name_given: str = ""
    lis_person_name_family: str = ""
    lis_person_name_full: str = ""
    ext_user_username: str = ""
    lis_person_contact_email_primary: str = ""
    launch_presentation_locale: str = ""
    ext_lms: str = ""
    tool_consumer_info_product_family_code: str = ""
    tool_consumer_info_version: str = ""
    oauth_callback: str = ""
    lti_version: str = ""
    lti_message_type: str = ""
    tool_consumer_instance_guid: str = ""
    tool_consumer_instance_name: str = ""
    tool_consumer_instance_description: str = ""
    launch_presentation_document_target: str = ""
    launch_presentation_return_url: str = ""
    oauth_signature_method: str = ""
    oauth_signature: str = ""
    custom_task_id: str = ""

    def as_form(self, **data) -> "LtiRequest":
        raise NotImplementedError

    @property
    def main_role(self) -> str:
        return self.roles[0]

    @property
    def pass_back_params(self) -> LtiPassBackParams:
        return LtiPassBackParams(
            lis_outcome_service_url=self.lis_outcome_service_url,
            lis_result_sourcedid=self.lis_result_sourcedid,
            oauth_consumer_key=self.oauth_consumer_key,
        )
