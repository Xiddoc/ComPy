"""
Native port for the Python builtin standard library.
"""
from typing import Dict, Any

from src.pybuiltins.PyPortFunctionSignature import PyPortFunctionSignature


# noinspection PyShadowingBuiltins,PyUnusedLocal
def print(print_string: Any) -> None:
	"""
	Prints a string to standard output.

	:param print_string: The string to print.
	"""


# noinspection PyUnusedLocal
def str_cast(obj: Any) -> str:
	"""
	Casts any object to a string, if possible.

	:param obj: The object to cast.
	:return: The string version of this object.
	"""


# noinspection PyUnusedLocal
def int_cast(obj: str) -> str:
	"""
	Casts a string object to an integer.

	:param obj: The string to cast.
	:return: The integer representation of this string.
	"""


# noinspection PyUnusedLocal
def inc(my_integer: int) -> int:
	"""
	Increments an integer.

	:param my_integer: The integer to increment.
	:return: The incremented value.
	"""


# noinspection PyShadowingBuiltins,PyUnusedLocal
def pow(value: int, exponent: int) -> int:
	"""
	Calculates a number to the power of the given exponent.

	:param value: The base value.
	:param exponent: The exponent's value.
	:return: The power of the base to the exponent.
	"""


objs: Dict[str, PyPortFunctionSignature] = {
	"print": PyPortFunctionSignature(
		function=print,
		code="std::cout<<print_string<<std::endl;",
		dependencies={"iostream"}
	),
	"str": PyPortFunctionSignature(
		function=str_cast,
		code="return std::to_string(obj);",
		dependencies={"iostream"}
	),
	"int": PyPortFunctionSignature(
		function=int_cast,
		code="return std::stoi(obj);",
		dependencies={"iostream"}
	),
	"inc": PyPortFunctionSignature(
		function=inc,
		code="return ++my_integer;"
	),
	"pow": PyPortFunctionSignature(
		function=pow,
		code="return pow(value, exponent);",
		dependencies={"cmath"}
	)
}
