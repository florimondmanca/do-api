"""Application factory."""

import falcon
import falcon_jsonify

from .middleware import CORS, ResponseLoggerMiddleware
from .resources import (ListDetailResource, ListResource, TaskDetailResource,
                        TaskResource)


def get_app() -> falcon.API:
    """Create and return an app instance."""
    middleware = [
        CORS(
            allow_all_methods=True,
            allow_all_origins=True,
            allowed_headers=['content-type'],
        ).middleware,
        ResponseLoggerMiddleware(),
        falcon_jsonify.Middleware(help_messages=True),
    ]

    app = falcon.API(middleware=middleware)

    app.add_route('/lists', ListResource())
    app.add_route('/lists/{id:int}', ListDetailResource())
    app.add_route('/tasks/', TaskResource())
    app.add_route('/tasks/{id:int}', TaskDetailResource())

    return app
