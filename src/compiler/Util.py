"""
Utility functions, methods, classes,
and other useful tools to help cut
and clean the code base.
"""
from _ast import AST
from functools import reduce
from typing import Union, Any, TYPE_CHECKING

# Type hint classes without executing code
if TYPE_CHECKING:
	from src.pybuiltins.PyPortFunction import PyPortFunction


class Util:
	"""
	Static utility class.
	"""

	@staticmethod
	def get_attr(obj: AST, attribute_path: str) -> Any:
		"""
		A function that recursively traverses down an "attribute path"
		and retrieves the value at the end of the path.

		This function exists since the CPython ast library uses an odd
		system which dynamically adds attributes to the AST instances,
		instead of statically declaring them in their respective classes.

		Due to this, mypy will throw a type-checking error since it will
		not find these attributes in the class defenition. Hence, to work
		around this bug, we will use the getattr function to retrieve the
		attributes directly.

		:param obj: The AST object to traverse.
		:param attribute_path: The attribute path to use (for example, if passing
								the object 'expression', and you want to navigate
								to the 'target' attribute, then the 'id' attribute
								of the 'target' attribute, then for this parameter
								you would pass the string "target.id").
		"""
		# Split by .
		# For example: "expression.target.id" becomes ["expression", "target", "id"]
		attrs = attribute_path.split(".")

		# Built in functools' reduce function to cumulatively execute the getattr function
		# On the first 2 arguments of the list
		return reduce(getattr, attrs, obj)

	@classmethod
	def get_name(cls, obj: AST) -> str:
		"""
		Retrieves the name of the AST node's class.
		For example, instead of seeing: <ast.AnnAssign object at 0x000002CC7FE5A310>
		You could use this method to abbreviate to: AnnAssign

		:param obj: An instance of the AST expression or node to name.
		:return: The string representation of the AST node's class name.
		"""
		return str(cls.get_attr(obj, "__class__.__name__"))

	@staticmethod
	def escape(string: str) -> str:
		"""
		Escapes a Python string of newlines
		and other formats in order to form
		a consistent one-line string.

		:param string: The string to escape.
		:return: The escaped one-line string.
		"""
		# Import locally to avoid cyclic import error
		from src.compiler.Constants import PY_SPECIAL_CHARS

		# For each special character
		for special_char, escaped_char in PY_SPECIAL_CHARS.items():
			# Replace with the escaped version
			string = string.replace(special_char, escaped_char)

		# Return escaped version
		return string
