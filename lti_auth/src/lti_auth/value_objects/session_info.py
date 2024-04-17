from dataclasses import dataclass


@dataclass(slots=True, kw_only=True)
class SessionInfo:
    timestamp: int
    """Метка времени"""
    nonce: str
    """Уникальный идентификатор"""
