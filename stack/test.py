import pytest
from stack import balance

test_data = [
    ('(((([{}]))))', True),
    ('[([])((([[[]]])))]{()}', True),
    ('{{[()]}}', True),
    ('}{}', False),
    ('{{[(])]}}', False),
    ('[[{())}]', False)
]


@pytest.mark.parametrize("string, result", test_data)
def test_is_string_balanced(string, result):
    assert balance.is_string_balanced(string) == result
