import pytest


@pytest.fixture()
def select_args():

    return ["users.name", "users.age", "estate.price"]


@pytest.fixture()
def from_args():

    return ["users", "estate", "id"]


@pytest.fixture()
def and_args():

    return {"users.name": "John Doe", "users.age": 25, "estate.price": 50000}


@pytest.fixture()
def or_args():

    return {"estate.type": "single floor home"}
