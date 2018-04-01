"""Simple CORS provider for Falcon."""

import falcon

ORIGIN_HEADER = 'Origin'
ALLOW_ORIGIN_HEADER = 'Access-Control-Allow-Origin'
REQUEST_HEADERS_HEADER = 'Access-Control-Request-Headers'
ALLOW_HEADERS_HEADER = 'Access-Control-Allow-Headers'
REQUEST_METHOD_HEADER = 'Access-Control-Request-Method'
ALLOW_METHODS_HEADER = 'Access-Control-Allow-Methods'
ALL = '*'


class CorsMiddleware:
    """Simple middleware that checks request origin."""

    def __init__(self, cors):
        self.cors = cors

    def process_request(self, request, response):
        """Main Falcon middleware hook."""
        return self.cors.process(request, response)


class CORS:
    """Wrapper to build a CORS middleware."""

    def __init__(self, allowed_origins=None,
                 allow_all_origins=False,
                 allowed_headers=None,
                 allow_all_headers=False,
                 allowed_methods=None,
                 allow_all_methods=False):
        # Origins
        if allow_all_origins:
            allowed_origins = [ALL]
        self.allowed_origins = allowed_origins or []
        # Headers
        if allow_all_headers:
            allowed_headers = [ALL]
        self.allowed_headers = allowed_headers or []
        # Methods
        if allow_all_methods:
            allowed_methods = [ALL]
        self.allowed_methods = allowed_methods or []
        self._normalize()

    def _normalize(self):
        self.allowed_headers = [header.lower()
                                for header in self.allowed_headers]
        self.allowed_methods = [method.upper()
                                for method in self.allowed_methods]

    def Middleware(self):
        """Build and return a CorsMiddleware object."""
        return CorsMiddleware(cors=self)

    def process(self, req, resp):
        method = req.get_header(REQUEST_METHOD_HEADER)
        self._process_method(req, resp, method)

        origin = req.get_header(ORIGIN_HEADER)
        if origin:
            self._process_origin(req, resp, origin)

        request_headers = req.get_header(REQUEST_HEADERS_HEADER)
        if request_headers:
            self._process_allowed_headers(req, resp, request_headers)

    def _allow(self, prop: str, value):
        allowed_values = getattr(self, 'allowed_' + prop)
        if ALL in allowed_values:
            return True
        return value.lower() in allowed_values

    def _process_method(self, req, resp, request_method):
        if self._allow('methods', request_method):
            resp.set_header(ALLOW_METHODS_HEADER, request_method)

    def _process_origin(self, req, resp, origin: str):
        if self._allow('origins', origin):
            resp.set_header(ALLOW_ORIGIN_HEADER, origin)

    def _process_allowed_headers(self, req, resp, request_headers: str):
        allowed_headers_list = [
            header for header in request_headers.split(',')
            if self._allow('headers', header)
        ]
        allowed_headers = ','.join(allowed_headers_list)
        resp.set_header(ALLOW_HEADERS_HEADER, allowed_headers)
