from enum import StrEnum


class StatEventType(StrEnum):
    open_page = "open_page"
    """Человек открыл задание страницы"""
    send_command = "send_command"
    """Человек ввёл команду"""
    resolve_task = "resolve_task"
    """Человек решил задачу"""
