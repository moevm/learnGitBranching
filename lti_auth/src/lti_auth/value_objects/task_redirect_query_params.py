from dataclasses import dataclass


@dataclass(slots=True)
class TaskRedirectQueryParams:
    """Query параметры для редиректа на задачу"""

    level_id: str
    """ID задачи"""
