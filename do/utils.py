"""Miscellaneous utilities."""

import falcon


def remove_empty(dictionnary) -> dict:
    """Remove items whose value is None in a dictionnary."""
    return {k: v for k, v in dictionnary.items() if v is not None}


def get_or_404(session, model, **kwargs):
    """Find an object matching all filters or raise a 404 error.

    Parameters
    ----------
    session : sqlalchemy.Session
    model : SQLAlchemy model
    **kwargs : dict
        A query on the model will be filtered using these values.
    """
    obj = session.query(model).filter_by(**kwargs).first()
    if not obj:
        raise falcon.HTTPNotFound()
    return obj
