from typing import Dict, List, Any, Callable

from flashcards.adapters.key_value_store.key_value_store import KeyValueStore, \
    Key, Value
from flashcards.adapters.key_value_store.query import Query, AndQuery, FieldEqual, FieldContains


class FakeKeyValueStore(KeyValueStore[Key, Value]):
    def __init__(
        self,
        values: Dict[Key, Value],
        dump_value: Callable[[Value], Dict[str, Any]],
    ):
        self._values = values
        self._dump_value = dump_value

    def get(self, key: Key) -> Value:
        return self._values[key]

    def set(self, key: Key, value: Value) -> None:
        self._values[key] = value

    def find(self, query: Query) -> List[Value]:
        return [
            value
            for value in self._values.values()
            if self._filter(query, value)
        ]

    def _filter(self, query: Query, value: Value) -> bool:
        if isinstance(query, AndQuery):
            return all(
                self._filter(clause, value)
                for clause in query.queries
            )
        if isinstance(query, FieldEqual):
            return self._dump_value(value)[query.field] == query.value
        if isinstance(query, FieldContains):
            return query.value in self._dump_value(value)[query.field]
        raise TypeError
