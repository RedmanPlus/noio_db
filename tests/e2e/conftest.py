import sqlite3

import pytest

from noio_db.models import Model
from noio_db.settings import Settings


class TestSettings(Settings):

    type: str = "sqlite"
    driver_path = "noio_db.core.db_drivers"
    db_name = "test"


class User(Model):

    name: str
    age: int
    email: str


@pytest.fixture()
def model():
    return User


@pytest.fixture()
def settings():
    return Settings


@pytest.fixture(scope="module")
def db():
    con = sqlite3.connect("test")
    cur = con.cursor()

    cur.execute(
        """
        CREATE TABLE user (
            id INTEGER PRIMARY KEY,
            name TEXT,
            age INTEGER,
            email TEXT
        );
        """
    )

    cur.execute(
        """
        INSERT INTO user (name, age, email)
        VALUES
            ("John Doe", 25, "foo@bar.com"),
            ("Jane Smith", 22, "bar@baz.com"),
            ("John Doe", 21, "foo@foo.com"),
            ("Jill Jizz", 25, "foo@baz.com"),
            ("Buck", 25, "bar@bar.com");
        """
    )

    con.commit()

    yield

    cur.execute(
        """
        DROP TABLE user;
        """
    )

    con.commit()
