"""Application factory."""

import falcon
import falcon_jsonify
from routes import routes
from helpers import add_routes, load_settings, get_session_factory
from middleware.cors import CORS
from middleware.logging import ResponseLoggerMiddleware
from middleware.sqlalchemy import SQLAlchemySessionManager


def create(settings_module_name=None) -> falcon.API:
    """Create and return an app instance."""
    settings = load_settings(module_name=settings_module_name)
    session_factory = get_session_factory(settings.DATABASE_URL)

    cors = CORS(
        allow_all_methods=True,
        allow_all_origins=True,
        allowed_headers=['content-type'],
    )

    middleware = [
        cors.Middleware(),
        falcon_jsonify.Middleware(help_messages=True),
        SQLAlchemySessionManager(factory=session_factory),
    ]
    if settings.LOG:
        middleware.append(ResponseLoggerMiddleware())

    app = falcon.API(middleware=middleware)
    add_routes(app, routes)

    return app
