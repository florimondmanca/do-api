"""Settings helpers."""

import os
from importlib import import_module
from types import SimpleNamespace


class Settings(SimpleNamespace):
    """Settings helper class."""


def load_settings(module_name: str=None) -> Settings:
    """Load settings from a Python module.

    Parameters
    ----------
    module_name : str, optional
    """
    if module_name is None:
        module_name = os.environ.get('SETTINGS_MODULE', None)
        if module_name is None:
            raise ImportError(
                'Cannot load settings - '
                'please pass the settings_module parameter of set the '
                'SETTINGS_MODULE environment variable.'
            )
    try:
        module = import_module(module_name)
        names = [name for name in dir(module) if not name.startswith("__")]
        settings = {name: getattr(module, name) for name in names}
        return Settings(**settings)
    except ImportError:
        raise
