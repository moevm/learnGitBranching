from starlette.datastructures import URL

from lti_auth.settings.settings import settings
from lti_auth.value_objects.url_components import UrlComponents


class JsTasksIntegrationService:
    @staticmethod
    def get_task_url(task_id: str) -> URL:
        """Получить url для задачи"""

        return UrlComponents(
            scheme="http",
            host_name=settings.nginx_host_name,
            host_port=settings.nginx_host_port,
            query=None,
            uri=settings.js_task_uri,
        ).url
