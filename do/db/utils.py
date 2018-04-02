"""Database utilities."""

from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

from .models import Base
from .settings import DATABASE_URL


# def create_tables():
#     """Utility function to create database tables."""
#     engine = create_engine(DATABASE_URL)
#     Base.metadata.create_all(engine)
#     print('Created database tables in {}'.format(DATABASE_URL))


def get_session_factory():
    """Create and return a session factory."""
    engine = create_engine(DATABASE_URL)
    Base.metadata.bind = engine
    return sessionmaker(bind=engine)


def get_session():
    """Convenience shortcut to create and return a database session."""
    factory = get_session_factory()
    return factory()
