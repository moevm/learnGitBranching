from typing import Any, ClassVar, Protocol, runtime_checkable


@runtime_checkable
class Dataclass(Protocol):
    __dataclass_fields__: ClassVar[dict[str, Any]]

    def __init__(self, **kwargs: Any) -> None:
        pass
