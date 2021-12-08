"""
Utility functions.
"""
from _ast import Constant

from Builtins import escaped_python_strings
from Errors import UnsupportedFeatureException


# def mangler(length: int) -> str:
# 	"""
# 	A function to return a mangled string of random characters.
# 	This is used often when you need to give an arbitrary name to a variable or object.
# 	For example, to function argument names (arbitrary and not relevant).
#
# 	:param length: The length of the mangled string to return.
# 	"""
# 	return ''.join(choice(ascii_letters) for _ in range(length))


def translate_constant(constant: Constant) -> str:
	"""
	Transpiles a constant to it's string representation.
	:param constant: The Constant object to transpile.
	"""
	# Get the contant's value type
	value_type = type(constant.value)
	# If the type is an integer or a boolean
	if value_type == int or value_type == bool:
		# Return the value
		return str(constant.value)

	elif value_type == str:
		# Encompass in quotes
		return f'"{escape_strings(constant.value)}"'

	else:
		# What type is that?
		# We can't use that
		raise UnsupportedFeatureException(f"Python type '{value_type}' is not supported by the compiler.")


def escape_strings(input_string: str) -> str:
	"""
	Takes a string object and escapes all sequences in the string before returning it.
	Sequences are \n, \r, and \t.

	:param input_string: The string to escape.
	"""
	# For each replacement
	for source, replacement in escaped_python_strings.items():
		# Perform the replacement
		input_string = input_string.replace(source, replacement)
	# Return the final string
	return input_string
