from dataclasses import dataclass, replace
from itertools import chain
from typing import NamedTuple, Type, Any, Tuple, Callable, Union, get_type_hints, Iterable

from infix import rbind
from pyrsistent import pvector, pmap
from pyrsistent.typing import PVector, PMap

from routedsl.bricks import DataType, URLTextFragment, empty_handler, Docstring


__all__ = (
    'Header', 'OK', 'GET', 'POST', 'PUT', 'PATCH', 'DELETE', 'HEAD', 'JSON',
    'HTTP',
)


Header = DataType()
JSON = DataType()


@dataclass(frozen=True)
class StatusCode:
    status: int
    typ: DataType = JSON[Type[Any]]

    def __getitem__(self, item: DataType) -> 'StatusCode':
        return replace(self, typ=item)


OK = StatusCode(200)

PlaceholderName = str

class HTTP(NamedTuple):
    method: str = 'GET'
    segments: PVector[URLTextFragment] = pvector(['/'])
    headers_type: Type[Any] = Type[Any]
    return_type: Tuple[int, DataType] = (200, JSON[Type[Any]])
    handler: Callable = empty_handler
    request_types: PMap[Type[Any], Type[Any]] = pmap()
    query_types: PMap[PlaceholderName, Tuple[Type[Any], Iterable[Docstring]]] = pmap()
    """ Set of types used in this HTTP segment
    """
    docs: Docstring = ""

    def __truediv__(self, other: Union[URLTextFragment, Union[Tuple[str, Type], Tuple[str, Type, Docstring]]]) -> 'HTTP':
        if isinstance(other, URLTextFragment):
            return self._replace(segments=pvector(chain(self.segments, [other])))

        elif isinstance(other, tuple):
            placeholder_name, typ, *docs = other
            if hasattr(typ, placeholder_name):
                typ_actual = get_type_hints(typ)[placeholder_name]
            else:
                typ_actual = typ

            return self._replace(
                segments=pvector(chain(self.segments, [f'{{{placeholder_name}}}'])),
                request_types=self.request_types.set(typ, typ).set(typ_actual, typ_actual),
                query_types=self.query_types.set(placeholder_name, (typ_actual, docs))
            )
        elif isinstance(other, rbind):
            return self | other

        raise NotImplementedError(f'Unknown type of URL segment: {type(other)}')

    @property
    def segments_url(self) -> str:
        url = '/'.join(x.strip('/ ') for x in self.segments if x.strip('/ '))
        return f'/{url}'

    def __repr__(self) -> str:
        return f'HTTP ( {self.method} {self.segments_url} )'


GET = HTTP('GET')
POST = HTTP('POST')
PUT = HTTP('PUT')
PATCH = HTTP('PATCH')
DELETE = HTTP('DELETE')
HEAD = HTTP('HEAD')
