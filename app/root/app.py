from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from app.root.settings.base import get_settings


def create_app():
    settings = get_settings()
    app = FastAPI(title=settings.PROJECT_NAME)

    setup_cors(app, settings)
    setup_routers(app, settings)
    return app


def setup_routers(app: FastAPI, settings):
    from app.apps.routers import router

    app.include_router(router, prefix=settings.API_V1_STR)


def setup_cors(app: FastAPI, settings):
    # TODO - its simplified for testing
    if settings.BACKEND_CORS_ORIGINS:
        app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )
