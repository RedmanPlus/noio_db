from importlib import import_module

from noio_db.core.db_drivers import BaseDriver
from noio_db.settings import Settings


def get_current_settings(obj) -> BaseDriver:
    if user_settings := Settings.__subclasses__():
        return import_module(user_settings[0]().driver_path).Driver(
            obj, user_settings[0]()
        )

    return import_module(Settings().driver_path).Driver(obj, Settings())
