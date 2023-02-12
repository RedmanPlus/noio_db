from typing import List

from noio_db.models import Model


def get_model_definitions() -> List[str]:
    definitions = []
    model_children = Model.__subclasses__()

    for child in model_children:

        definitions.append(child.create())

    return definitions
