"""Application factory."""

import falcon
import falcon_jsonify
from db import get_session_factory
from middleware.cors import CORS
from middleware.logging import ResponseLoggerMiddleware
from middleware.sqlalchemy import SQLAlchemySessionManager
from resources import (ListDetailResource, ListResource, TaskDetailResource,
                       TaskResource)


def get_app() -> falcon.API:
    """Create and return an app instance."""
    # Setup database
    session_factory = get_session_factory()

    # Configure CORS
    cors = CORS(
        allow_all_methods=True,
        allow_all_origins=True,
        allowed_headers=['content-type'],
    )

    # Create middlewares
    middleware = [
        cors.Middleware(),
        falcon_jsonify.Middleware(help_messages=True),
        SQLAlchemySessionManager(factory=session_factory),
        ResponseLoggerMiddleware(),
    ]

    # Instanciate application
    app = falcon.API(middleware=middleware)

    # Configure routes
    app.add_route('/lists', ListResource())
    app.add_route('/lists/{id:int}', ListDetailResource())
    app.add_route('/tasks/', TaskResource())
    app.add_route('/tasks/{id:int}', TaskDetailResource())

    return app
