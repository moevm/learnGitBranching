from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware import Middleware

from lti_auth.web.middlewares.handle_errors import HandleErrorsMiddleware

app_middleware_collection = [
    Middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    ),
    Middleware(HandleErrorsMiddleware),
]
