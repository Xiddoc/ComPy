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


# noinspection PyUnusedLocal,PyShadowingBuiltins
def input(print_string: str) -> str:
	"""
	Takes input from the user.

	:param print_string: A string to print before taking input.
	:return: The user input, until the user presses the Enter key.
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


# noinspection PyShadowingBuiltins,PyUnusedLocal
def pow(value: int, exponent: int) -> int:
	"""
	Calculates a number to the power of the given exponent.

	:param value: The base value.
	:param exponent: The exponent's value.
	:return: The power of the base to the exponent.
	"""


ported_objs: Dict[str, PyPortFunctionSignature] = {
	"print": PyPortFunctionSignature(
		function=print,
		code="std::cout<<print_string<<std::endl;",
		dependencies={"iostream"}
	),
	"input": PyPortFunctionSignature(
		function=input,
		code="print(std::move(print_string));std::string s;std::cin>>s;return s;",
		dependencies={"iostream", "utility"},
		linked_ports={"print"}
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
	"pow": PyPortFunctionSignature(
		function=pow,
		code="return pow(value, exponent);",
		dependencies={"cmath"}
	)
}
