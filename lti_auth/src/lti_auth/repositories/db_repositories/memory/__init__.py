from lti_auth.repositories.db_repositories.memory.lti_sessions import (
    MemoryLtiSessionsRepository,
)
from lti_auth.repositories.db_repositories.memory.users import MemoryUsersRepository

lti_sessions_repository = MemoryLtiSessionsRepository()
user_repository = MemoryUsersRepository()
