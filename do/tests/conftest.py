"""Pytest fixtures declaration."""
import os
from datetime import datetime

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
    os.environ['SETTINGS_MODULE'] = 'settings.testing'

    yield load_settings()

    if previous:
        print('Unsetting test settings...')
        os.environ['SETTINGS_MODULE'] = previous


@pytest.fixture(scope='module')
def session(settings):
    """Provide a module-scoped test database."""
    print('Create test database...')
    apply_migrations()

    yield get_session(database_url=settings.DATABASE_URL)

    print('Removing test database...')
    delete_database(name=settings.DATABASE_NAME)


@pytest.fixture()
def client(settings, session):
    """Setup and return a test client."""
    return Client(app.create())


@pytest.fixture()
def now():
    """Return current date and time as a Python datetime object."""
    return datetime.now()


@pytest.fixture()
def list_title():
    """Return an example list title."""
    return 'Shopping'


@pytest.fixture()
def task_payload(now):
    """Return an example valid task payload, with all possible parameters."""
    return {
        'title': 'Eat donuts',
        'list_id': 1,
        'due_date': str(now),
        'priority': 2,
        'completed': False,
    }
