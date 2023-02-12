import pytest


class TestDelete:
    # pylint: disable=W0613
    @pytest.mark.e2e
    def test_delete_one_obj(self, model, settings, db, snapshot):

        query = model.filter(age=25)
        first = query[0]

        first.delete()

        query = model.filter(age=25)
        snapshot.assert_match(str(query.to_json()), "delete_obj")

    # pylint: enable=W0613
