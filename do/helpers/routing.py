"""Routing helpers."""

import falcon


def add_routes(app: falcon.API, routes: dict):
    """Add routes to a Falcon app from a uri-resource mapping."""
    for uri_template, resource in routes.items():
        app.add_route(uri_template, resource)
