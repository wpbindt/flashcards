from abc import abstractmethod, ABC
from typing import Generic, TypeVar, Hashable, Any

IdType = TypeVar('IdType', bound=Hashable)


class Entity(ABC, Generic[IdType]):
    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, type(self)):
            return False
        return self.id == other.id

    def __hash__(self) -> int:
        return hash(self.id)

    @property
    @abstractmethod
    def id(self) -> IdType:
        pass
