from hypothesis import given
from hypothesis import strategies as st

from check_nested_loops import find_nested_loop_lines

FLAT = "def f(items):\n    for item in items:\n        print(item)\n"
NESTED = "def f(rows):\n    for row in rows:\n        for cell in row:\n            print(cell)\n"
WHILE_IN_FOR = "def f(a):\n    for x in a:\n        while x:\n            x -= 1\n"
DOUBLE_COMPREHENSION = "def f(m):\n    return [c for r in m for c in r]\n"
COMPREHENSION_IN_LOOP = "def f(m):\n    for r in m:\n        print([c for c in r])\n"
SEPARATE_FUNCTIONS = (
    "def f(a):\n    for x in a:\n        def g(b):\n            for y in b:\n"
    "                print(y)\n        g(x)\n"
)


def test_flat_loop_is_accepted() -> None:
    assert find_nested_loop_lines(FLAT) == []


def test_for_in_for_is_reported() -> None:
    assert find_nested_loop_lines(NESTED) == [3]


def test_while_in_for_is_reported() -> None:
    assert find_nested_loop_lines(WHILE_IN_FOR) == [3]


def test_comprehension_with_two_for_clauses_is_reported() -> None:
    assert find_nested_loop_lines(DOUBLE_COMPREHENSION) == [2]


def test_comprehension_inside_loop_is_reported() -> None:
    assert find_nested_loop_lines(COMPREHENSION_IN_LOOP) == [3]


def test_inner_function_starts_fresh() -> None:
    assert find_nested_loop_lines(SEPARATE_FUNCTIONS) == []


@given(st.integers(min_value=1, max_value=8))
def test_sequential_loops_never_count_as_nested(count: int) -> None:
    body = "".join("    for i in a:\n        pass\n" for _ in range(count))
    assert find_nested_loop_lines(f"def f(a):\n{body}") == []
