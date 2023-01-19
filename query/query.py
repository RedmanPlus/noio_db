from typing import List, Dict
from models import BaseNoIoObject


class Query:

    def __init__(self):

        self.objects: List[BaseNoIoObject] = []
        self.query_ast: Dict[str, str] | None = None

    def __getitem__(self, item):
        pass