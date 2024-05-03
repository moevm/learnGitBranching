import random
from datetime import datetime

from locust import TaskSet, task, HttpUser, between
from locust.clients import LocustResponse
from oauthlib.oauth1.rfc5849.signature import normalize_parameters, base_string_uri, signature_base_string, _sign_hmac



class WebSiteUser(HttpUser):
    wait_time = between(0, 1)

    params_order = ['oauth_version', 'oauth_nonce', 'oauth_timestamp', 'oauth_consumer_key', 'user_id',
                    'lis_person_sourcedid', 'roles', 'context_id', 'context_label', 'context_title',
                    'resource_link_title', 'resource_link_description', 'resource_link_id', 'context_type',
                    'lis_course_section_sourcedid', 'lis_result_sourcedid', 'lis_outcome_service_url',
                    'lis_person_name_given', 'lis_person_name_family', 'lis_person_name_full', 'ext_user_username',
                    'lis_person_contact_email_primary', 'launch_presentation_locale', 'ext_lms',
                    'tool_consumer_info_product_family_code', 'tool_consumer_info_version', 'oauth_callback',
                    'lti_version', 'lti_message_type', 'tool_consumer_instance_guid', 'tool_consumer_instance_name',
                    'tool_consumer_instance_description', 'custom_task_id', 'launch_presentation_document_target',
                    'launch_presentation_return_url', 'oauth_signature_method']
    hash_algorithm_name = 'SHA-1'
    client_secret = 'secretkey'
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Accept-Language': 'ru,en;q=0.9',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Origin': 'https://e.moevm.info',
        'Referer': 'https://e.moevm.info/',
        'Sec-Fetch-Dest': 'iframe',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'cross-site',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 YaBrowser/24.1.0.0 Safari/537.36',
        'sec-ch-ua': '"Not_A Brand";v="8", "Chromium";v="120", "YaBrowser";v="24.1", "Yowser";v="2.5"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
    }

    def on_start(self) -> None:
        pass

    def _gen_payload(self) -> dict[str, str]:
        data = {
            'oauth_version': '1.0',
            'oauth_nonce': 'd18f845eb25b2a0113753e41a28ab526',
            'oauth_timestamp': '1714700726',
            'oauth_consumer_key': 'publickey',
            'user_id': f'{random.randint(100, 1000)}',
            'lis_person_sourcedid': '',
            'roles': 'Instructor',
            'context_id': '88',
            'context_label': 'Курс для тестирования learnGitBranching',
            'context_title': 'Курс для тестирования learnGitBranching',
            'resource_link_title': 'тестовое локально не в докере',
            'resource_link_description': '',
            'resource_link_id': '539',
            'context_type': 'CourseSection',
            'lis_course_section_sourcedid': '',
            'lis_result_sourcedid': '{"data":{"instanceid":"539","userid":"286","typeid":"34","launchid":1544112258},"hash":"584d13d29d7a13695b5706c51ffde7c3aa070b6d7d45a02d7c05f40ed869d3ac"}',
            'lis_outcome_service_url': 'https://e.moevm.info/mod/lti/service.php',
            'lis_person_name_given': 'Михаил',
            'lis_person_name_family': 'Переверза',
            'lis_person_name_full': 'Михаил Переверза',
            'ext_user_username': 'pereverzacrazy',
            'lis_person_contact_email_primary': 'pereverzamihail@gmail.com',
            'launch_presentation_locale': 'ru',
            'ext_lms': 'moodle-2',
            'tool_consumer_info_product_family_code': 'moodle',
            'tool_consumer_info_version': '2019111802.01',
            'oauth_callback': 'about:blank',
            'lti_version': 'LTI-1p0',
            'lti_message_type': 'basic-lti-launch-request',
            'tool_consumer_instance_guid': 'e.moevm.info',
            'tool_consumer_instance_name': 'moevm',
            'tool_consumer_instance_description': 'e.moevm.info',
            'custom_task_id': 'intro1',
            'launch_presentation_document_target': 'iframe',
            'launch_presentation_return_url': 'https://e.moevm.info/mod/lti/return.php?course=88&launch_container=3&instanceid=539&sesskey=PRiTGWmsqL',
            'oauth_signature_method': 'HMAC-SHA1',
            'oauth_signature': 'nLMWdgbzj/6MDLsoU623Cx4QkvA=',
        }
        return data

    def _generate_signature(self, data: dict[str, str]) -> str:
        norm_params = normalize_parameters([(key, data[key]) for key in self.params_order])
        bs_uri = base_string_uri('https://localhost/python_app/public/v1/lti/')

        sig_base_str = signature_base_string('POST', bs_uri, norm_params)
        signature = _sign_hmac(self.hash_algorithm_name, sig_base_str, self.client_secret, None)

        return signature

    @task(1000)
    def lti_auth(self):
        data = self._gen_payload()
        data['oauth_signature'] = self._generate_signature(data=data)
        response: LocustResponse = self.client.post("/python_app/public/v1/lti/", data=data, headers=self.headers, verify=False, allow_redirects=False)
        # print(response)
        # print(type(response))
        # print(response.status_code)
        # print(response.text)