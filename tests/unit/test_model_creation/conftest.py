import pytest

from noio_db import models


class Test(models.Model):

    id: int
    name: str
    age: int
    salary: int
    is_married: bool


@pytest.fixture()
def test():

    return Test
