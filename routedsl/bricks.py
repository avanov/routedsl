from dataclasses import dataclass, replace
from typing import Type, Any, Tuple

URLTextFragment = str
Docstring = str


@dataclass(frozen=True)
class DataType:
    typ: Type[Any] = Type[Any]

    def __getitem__(self, item: Type[Any]) -> 'DataType':
        return replace(self, typ=item)


def empty_handler() -> Tuple[()]:
    """ A stub function that represents a handler that does nothing
    """
    return ()
