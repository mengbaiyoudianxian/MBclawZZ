from fastapi import FastAPI

from .api import app
from .governor import Governor
from .middleware import GovernorMiddleware


def create_app():
    g = Governor()

    application = FastAPI(title="Governor Runtime")

    application.add_middleware(GovernorMiddleware, governor=g)

    application.mount("/v1", app)

    return application


app = create_app()
