"""SQLAlchemy session management middleware.

Inspired by:
https://eshlox.net/2017/07/28/integrate-sqlalchemy-with-falcon-framework/
"""

from sqlalchemy.orm import scoped_session, sessionmaker


class SQLAlchemySessionManager:
    """Create scoped session for every request, close it when request ends."""

    def __init__(self, factory: sessionmaker):
        self.scoped_session_factory = scoped_session(factory)

    def process_resource(self, req, resp, resource, params):
        """Attach the session to the resource."""
        resource.session = self.scoped_session_factory()

    def process_response(self, req, resp, resource, req_succeeded):
        """Close the session in the resource, if any."""
        if hasattr(resource, 'session'):
            if not req_succeeded:
                resource.session.rollback()
            self.scoped_session_factory.remove()
