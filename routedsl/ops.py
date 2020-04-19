from typing import Type, Any, Union, Callable

from infix import or_infix as infix

from routedsl.bricks import DataType, Docstring
from routedsl.http import HTTP, StatusCode

__all__ = (
    'HEADERS',
    'PAYLOAD',
    'RETURNS',
    'HANDLER',
    'GUARDS',
    'IS',
    'LIKE',
    'DOCS',
)


@infix
def HEADERS(a: HTTP, b: Type) -> HTTP:
    return a._replace(headers_type=b)


@infix
def PAYLOAD(a: HTTP, b: DataType) -> HTTP:
    return a._replace(request_types=a.request_types.set(b.typ, b.typ))


@infix
def RETURNS(a: HTTP, b: Union[StatusCode, DataType]) -> HTTP:
    if isinstance(b, StatusCode):
        status = b.status
        typ = b.typ
    else:
        status = 200
        typ = b
    return a._replace(return_type=(status, typ))


@infix
def HANDLER(a: HTTP, b: Callable) -> HTTP:
    # TODO: compare handler return type with HTTP.return_type
    return a._replace(handler=b)


@infix
def GUARDS(a: HTTP, b: Any) -> HTTP:
    return a


@infix
def IS(a: property, b: Any) -> Any:
    return a


@infix
def LIKE(a: HTTP, b: Any) -> HTTP:
    return a


@infix
def DOCS(a: HTTP, b: Docstring) -> 'HTTP':
    return a._replace(docs=f'{a.docs}\n\n{b}')
