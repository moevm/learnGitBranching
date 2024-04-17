from typing import Generic, NamedTuple, TypeVar
from urllib.parse import urlencode

from serpyco_rs import Serializer
from starlette.datastructures import URL

from lti_auth.utils.types import Dataclass

_T = TypeVar("_T", bound=Dataclass)
_serializers: dict[type[Dataclass], Serializer] = {}


class UrlComponents(Generic[_T], NamedTuple):
    scheme: str
    """Схема URL"""
    host_name: str
    """Имя хоста"""
    host_port: int | str | None
    """Порт"""
    uri: str
    """URL"""
    query: _T | None = None
    """Параметры запроса"""
    fragment: str | None = None
    """Фрагмент"""

    @property
    def url(self) -> URL:
        return _base_url.replace(
            hostname=self.host_name,
            port=self.str_port,
            path=self.uri,
            query=self._encoded_query,
            fragment=self.fragment,
        )

    @property
    def str_port(self) -> str | None:
        if self.host_port is None:
            return None
        return str(self.host_port)

    @property
    def _encoded_query(self) -> str | None:
        if self._query_serializer is None:
            return None
        return urlencode(self._query_serializer.dump(self.query))

    @property
    def _query_serializer(self) -> Serializer | None:
        if self.query is None:
            return None

        serializer = _serializers.get(type(self.query))
        if serializer is None:
            serializer = _serializers.setdefault(type(self.query), Serializer(type(self.query)))

        return serializer


# Задаём базовый url, который и будем реплейсить, т.к. с нуля создавать со значениями port не даёт, только с netloc
_base_url = URL("https://localhost:8000")
