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

    log_format = (
        "{req.scheme} {req.method} {req.relative_uri}"
        "{status_code} {req.host} {req.user_agent}"
    )

    def __init__(self, logger=None, log_format=None):
        if not logger:
            logger = default_logger
        if log_format is not None:
            self.log_format = log_format
        self.logger = logger

    def process_resource(self, req, resp, resource, params):
        """Make logger available to resource classes."""
        resource.logger = self.logger

    def process_response(self, req, resp, resource, req_succeeded):
        """Output request and response info to logger."""
        self.logger.info(self.log_format.format(
            req=req, resp=resp, status_code=resp.status[:3]
        ))
