"""Testing settings."""

import os

DATABASE_URL = os.environ.get(
    'DATABASE_URL', 'postgres://postgres:postgres@localhost:5432/do_api_test')
LOG = False
