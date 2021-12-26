"""
Native port for the Python builtin standard library.
"""
from typing import Dict

from src.pybuiltins.PyPort import PyPort


# noinspection PyShadowingBuiltins
def print(print_string: str) -> None:
	"""
	Prints a string to standard output.
	@param print_string: The string to print.
	"""


def inc(my_integer: int) -> int:
	"""
	Increments an integer.

	@param my_integer: The integer to increment.
	@return: The incremented value.
	"""


# noinspection PyShadowingBuiltins
def pow(value: int, exponent: int) -> int:
	"""
	Calculates a number to the power of the given exponent.

	@param value: The base value.
	@param exponent: The exponent's value.
	@return: The power of the base to the exponent.
	"""


objs: Dict[str, PyPort] = {
	"print": PyPort(
		obj=print,
		code="cout << print_string << endl;"
	),
	"inc": PyPort(
		obj=inc,
		code="return ++my_integer;"
	),
	"pow": PyPort(
		obj=pow,
		code="return pow(value, exponent);",
		dependencies={"cmath"}
	)
}
