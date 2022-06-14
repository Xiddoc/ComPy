"""
Example of a ported library.
"""

from typing import Dict

from src import PyPortFunctionSignature


# noinspection PyUnusedLocal
def add(number_one: int, number_two: int) -> int:
    """
    Adds two numbers.
    """


# noinspection PyUnusedName
ported_objs: Dict[str, PyPortFunctionSignature] = {
    "add": PyPortFunctionSignature(
        function=add,
        code="return number_one + number_two;"
    )
}
