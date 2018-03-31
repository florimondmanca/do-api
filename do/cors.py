"""Simple CORS provider for Falcon."""

ORIGIN_HEADER = 'Origin'
ALLOW_ORIGIN_HEADER = 'Access-Control-Allow-Origin'
ALL_ORIGINS = '*'


class CorsMiddleware:
    """Simple middleware that checks request origin."""

    def __init__(self, allowed_origins):
        self.allowed_origins = allowed_origins

    def allow(self, origin):
        """Return whether the origin is allowed."""
        if ALL_ORIGINS in self.allowed_origins:
            return True
        return origin in self.allowed_origins

    def process_request(self, request, response):
        """Middleware hook."""
        origin = request.get_header(ORIGIN_HEADER)
        if self.allow(origin):
            response.set_header(ALLOW_ORIGIN_HEADER, origin)


class CORS:
    """Light wrapper to build a CORS middleware.

    Parameters
    ----------
    allowed_origins : list of str, optional ([])
    allow_all_origins : boolean, optional (False)
    """

    def __init__(self, allowed_origins=None,
                 allow_all_origins=False):
        if allow_all_origins:
            allowed_origins = [ALL_ORIGINS]
        self.allowed_origins = allowed_origins or []

    @property
    def middleware(self):
        """Build and return a CorsMiddleware object."""
        return CorsMiddleware(allowed_origins=self.allowed_origins)
