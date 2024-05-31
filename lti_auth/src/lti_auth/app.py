import nest_asyncio  # type: ignore[import-untyped]
from fastapi import FastAPI

from lti_auth.enums.web.request_method import RequestMethod
from lti_auth.repositories.db_repositories.mongo import client
from lti_auth.repositories.db_repositories.mongo.init_db import init_db
from lti_auth.web.handlers.app_handlers import app_handlers
from lti_auth.web.middlewares import app_middleware_collection

nest_asyncio.apply()


app = FastAPI(
    openapi_url="/core/openapi.json",
    docs_url="/core/docs",
    middleware=app_middleware_collection,
)


@app.on_event("startup")
async def on_startup() -> None:
    await init_db()


@app.on_event("shutdown")
async def on_shutdown() -> None:
    client.close()


for handler in app_handlers:
    match handler.method:
        case RequestMethod.get:
            app_method = app.get
        case RequestMethod.post:
            app_method = app.post
        case _:
            raise AssertionError(f"Метод {handler.method} не поддерживается")

    app_method(path=handler.path)(handler.controller)
