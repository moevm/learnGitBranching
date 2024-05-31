from serpyco_rs import Serializer

from lti_auth.entities.domain.user import BaseUser, TaskUser

base_user_serializer = Serializer(BaseUser)
task_user_serializer = Serializer(TaskUser)
