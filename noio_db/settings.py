from pydantic import BaseSettings


class Settings(BaseSettings):

    type: str
    driver_path: str = "noio_db.core.db_drivers.sqlite_driver"
    db_name: str
