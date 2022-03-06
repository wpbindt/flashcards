from abc import ABC, abstractmethod
from typing import Generic, Hashable, TypeVar, List

from flashcards.adapters.key_value_store.query import Query

Key = TypeVar('Key', bound=Hashable)
Value = TypeVar('Value')


class KeyValueStore(ABC, Generic[Key, Value]):
    @abstractmethod
    def get(self, key: Key) -> Value:
        ...

    @abstractmethod
    def set(self, key: Key, value: Value) -> None:
        ...

    @abstractmethod
    def find(self, query: Query) -> List[Value]:
        ...
