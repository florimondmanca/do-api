"""Miscellaneous utilities."""

from typing import Union

import falcon


def find_or(error, collection,
            index=False, with_index=False, **kwargs) -> Union[int, dict]:
    """Find an item matching criteria in a collection, or raise an error.

    Parameters
    ----------
    error : Exception
    collection : iterable
    index : boolean, optional (default: False)
        Determines what is returned by this function.
    with_index: boolean, optional (default: False)
        Determines what is returned by this function.
    **kwargs : dict
        Key-value pairs to filter through the collection and find the item.

    Returns
    -------
    result : object or int
        If with_index=True, the position of the item and the item object.
        If index=True, the position of the item only.
        Otherwise, the item object only.
    """
    for i, item in enumerate(collection):
        try:
            found = all(item[k] == v for k, v in kwargs.items())
        except KeyError as e:
            raise KeyError('{} is not a valid lookup key in this collection'
                           .format(e.args[0]))
        if found:
            if with_index:
                return i, item
            if index:
                return i
            return item
    if error:
        raise error


def find_or_404(*args, **kwargs):
    return find_or(falcon.HTTPNotFound, *args, **kwargs)


def find_or_500(*args, **kwargs):
    return find_or(falcon.HTTPInternalServerError, *args, **kwargs)


def find_maybe(*args, **kwargs):
    return find_or(None, *args, **kwargs)


def query(collection, **kwargs) -> dict:
    """Find all items in a collection that meet criteria.

    Note: this is a generator.
    """
    for item in collection:
        if all(item[k] == v for k, v in kwargs.items()):
            yield item


def remove_empty(dictionnary) -> dict:
    """Remove items whose value is None in a dictionnary."""
    return {k: v for k, v in dictionnary.items() if v is not None}
