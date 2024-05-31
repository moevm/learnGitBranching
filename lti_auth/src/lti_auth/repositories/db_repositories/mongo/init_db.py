from lti_auth.repositories.db_repositories.mongo import consumers_collection
from lti_auth.settings.settings import settings


async def init_db() -> None:
    await consumers_collection.insert_one(
        {
            "oauth_consumer_key": settings.session_public_key,
            "oauth_consumer_secret": settings.session_secret_key,
        },
    )
