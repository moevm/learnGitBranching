from motor.core import AgnosticClient, AgnosticCollection, AgnosticDatabase
from motor.motor_asyncio import AsyncIOMotorClient

from lti_auth.repositories.db_repositories.mongo.lti_sessions import LtiSessionsMongoRepository
from lti_auth.repositories.db_repositories.mongo.stat_events import StatEventsMongoRepository
from lti_auth.repositories.db_repositories.mongo.users import UsersMongoRepository
from lti_auth.settings.settings import settings

client: AgnosticClient = AsyncIOMotorClient(settings.mongo_url)
db: AgnosticDatabase = client["learn-git"]


users_collection: AgnosticCollection = db["users"]
consumers_collection: AgnosticCollection = db["consumers"]
stat_events_collection: AgnosticCollection = db["stat_events"]


users_mongo_repository = UsersMongoRepository(users_collection=users_collection)
lti_sessions_mongo_repository = LtiSessionsMongoRepository(consumers_collection=consumers_collection)
stat_events_mongo_repository = StatEventsMongoRepository(stat_events_collection=stat_events_collection)
