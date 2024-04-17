from dataclasses import dataclass


@dataclass(kw_only=True)
class LtiPassBackParams:
    lis_outcome_service_url: str
    """URL для передачи оценки"""
    lis_result_sourcedid: str
    """Идентификатор результата"""
    oauth_consumer_key: str
    """Ключ для OAuth"""
