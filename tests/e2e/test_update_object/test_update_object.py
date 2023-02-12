import pytest


class TestUpdate:
    # pylint: disable=W0613
    @pytest.mark.e2e
    def test_update_model_from_db(self, model, small_db, snapshot):

        query = model.filter(name="Jane", age=25, email="my_email@mail.ru")
        jane = query[0]

        jane.age += 1
        jane.email = "my_new_email@mail.ru"

        jane.save()

        query = model.filter(name="Jane")
        snapshot.assert_match(str(query.to_json()), "update_obj")

    # pylint: enable=W0613
