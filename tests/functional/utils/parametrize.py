import pytest


QUERY_EXIST = 'PYTESTFILMS'
QUERY_NOT_EXIST = 'NOTEXIST'


film_search_parameters = [
    (
        {'query': QUERY_EXIST, 'page_number': 1, 'page_size': 10},
        {'status': 200, 'length': 50, 'has_next_page': f'/films/search?query={QUERY_EXIST}&page=2'}
    ),
    (
        {'query': QUERY_NOT_EXIST, 'page_number': 1, 'page_size': 10},
        {'status': 200, 'length': 0, 'has_next_page': None}
    )
]