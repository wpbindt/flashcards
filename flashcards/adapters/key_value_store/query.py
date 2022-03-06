from dataclasses import dataclass
from typing import Sequence, Any


class Query:
    ...


@dataclass(frozen=True)
class FieldEqual(Query):
    field: str
    value: Any


@dataclass(frozen=True)
class AndQuery(Query):
    queries: Sequence[Query]
