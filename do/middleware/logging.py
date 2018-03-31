"""Logging middleware."""

import logging

default_logger = logging.getLogger(__name__)
handler = logging.StreamHandler()
formatter = logging.Formatter(
    '[%(asctime)s] [%(process)d] [%(levelname)s] %(message)s')
handler.setFormatter(formatter)
default_logger.addHandler(handler)
default_logger.setLevel(logging.INFO)


class ResponseLoggerMiddleware:
    """Simple response logger middleware."""

    def __init__(self, logger=None):
        if not logger:
            logger = default_logger
        self.logger = logger

    def process_response(self, req, resp, resource, req_succeeded):
        self.logger.info(f'"{req.scheme} {req.method} \
{req.relative_uri}" {resp.status[:3]} "{req.host}" "{req.user_agent}"')
