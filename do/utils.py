"""Miscellaneous utilities."""

from typing import Union
import falcon


def find_or_404(collection, index=False, **kwargs) -> Union[int, dict]:
    """Find an item matching criteria in a collection, or faise a 404 error.

    Parameters
    ----------
    collection : iterable
    index : boolean, optional (default: False)
        Determines what is returned by this function.
    **kwargs : dict
        Key-value pairs to filter through the collection and find the item.

    Returns
    -------
    item : object or int
        If index=True, returns the position of the item in the collection,
        otherwise returns the item object itself.
    """
    for i, item in enumerate(collection):
        if all(item[k] == v for k, v in kwargs.items()):
            if index:
                return i
            return item
    raise falcon.HTTPNotFound()


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
