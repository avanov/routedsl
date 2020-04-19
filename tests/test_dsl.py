from typing import NamedTuple

from routedsl import *
from routedsl.bricks import empty_handler
from routedsl.dsl import generate_router


def test_dsl_composition() -> None:

    class User(NamedTuple):
        user_id: int

    class Headers(NamedTuple):
        content_type: str = 'application/json'

    def get_user_info() -> User:
        return User(user_id=1)

    def update_user_info(user: User) -> bool:
        return True

    DefaultHandler = HANDLER | get_user_info

    routes = Routes() (
        GET / 'users' / ('user_id', User, "User identifier")
        | HEADERS | Headers
        | RETURNS | JSON[ User]
        | DefaultHandler
        | GUARDS | (Headers.content_type | IS | 'application/json'
                    )
        | DOCS | """Get a user profile in JSON format"""
    )(
        POST / 'users' / ('user_id', User)
        | HEADERS | Headers
        | PAYLOAD | JSON[ User]
        | RETURNS | OK [ JSON[ bool]]
        | HANDLER | update_user_info
    )

    routes = (routes / 'users' / ('user_id', User)) (
        POST / 'edit'
        | HEADERS | Headers
        | RETURNS | JSON[ User]
        | HANDLER | update_user_info
    )

    DefaultHeaders = HEADERS | Headers
    DefaultHandler = HANDLER | empty_handler

    DefaultEndpoint = GET / DefaultHeaders | DefaultHandler

    routes3 = Routes() | DefaultEndpoint

    print(routes)

    router, type_constructors = generate_router(routes)
    matched_map, route = router.mapper.routematch(url='/users/4', environ={})
    schema: HTTP = route._kargs['controller']
    print(matched_map)
    query_args = {name: schema.query_types[name][0](val) for name, val in matched_map.items() if name in route.minkeys}
    assert isinstance(query_args['user_id'], int)
