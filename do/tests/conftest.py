"""Pytest fixtures declaration."""
import os

import pytest

from do import app
from falcon.testing import TestClient as Client
from helpers.db import apply_migrations, delete_database, get_session
from helpers.settings import load_settings


@pytest.fixture(scope='session')
def settings():
    """Expose app settings in tests."""
    print('Loading test settings...')
    previous = os.environ.get('SETTINGS_MODULE', None)
    os.environ.setdefault('SETTINGS_MODULE', 'settings.testing')

    yield load_settings()

    if previous:
        print('Unsetting test settings...')
        os.environ.setdefault('SETTINGS_MODULE', previous)


@pytest.fixture(scope='module')
def session(settings):
    """Provide a module-scoped test database."""
    print('Create test database...')
    apply_migrations()

    yield get_session(database_url=settings.DATABASE_URL)

    print('Removing test database...')
    delete_database(name=settings.DATABASE_NAME)


@pytest.fixture()
def client(settings):
    """Setup and return a test client."""
    return Client(app.create())
