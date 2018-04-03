"""Database utilities."""

from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.engine.url import make_url
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils.functions import (create_database, database_exists,
                                        drop_database)

from helpers.shell import success
from models import Base

ALEMBIC_UPGRADE_HEAD = ['alembic', 'upgrade', 'head']
ALEMBIC_GENERATE = ['alembic', 'revision', '--autogenerate']


def get_session_factory(database_url: str) -> sessionmaker:
    """Create and return a session factory."""
    engine: Engine = create_engine(database_url)
    Base.metadata.bind = engine
    return sessionmaker(bind=engine)


def create_migrations(message):
    """Create autogenerated Alembic migrations."""
    message_opts = message and ['-m', message] or []
    if success([*ALEMBIC_GENERATE, *message_opts]):
        print('OK')


def apply_migrations():
    """Apply Alembic migrations."""
    return success(ALEMBIC_UPGRADE_HEAD)


class DatabaseBackend:

    def __init__(self, settings):
        self.url = make_url(settings.DATABASE_URL)

    def create(self):
        create_database(self.url)

    def drop(self):
        drop_database(self.url)

    def exists(self):
        return database_exists(self.url)
