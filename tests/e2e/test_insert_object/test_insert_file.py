import pytest


class TestInsert:
    # pylint: disable=W0613
    @pytest.mark.e2e
    def test_insert_object(self, model, settings, db, snapshot):
        jane = model(name="Jane", age=24, email="jane_cool@mail.com")
        jane.Config.is_from_orm = False
        jane.save()

        query = model.all()
        snapshot.assert_match(str(query.to_json()), "insert_obj")

    # pylint: enable=W0613
