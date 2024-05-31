from dataclasses import dataclass


@dataclass
class SendMarkRequestV1:
    mark: float
    """Оценка"""
