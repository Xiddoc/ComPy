"""
PyExpression base class.
Used in extending for other expressions.
"""
from _ast import expr
from abc import abstractmethod, ABCMeta
from typing import List

from Errors import UnsupportedFeatureException


# noinspection PyUnusedFunction
class PyExpression(metaclass=ABCMeta):
	"""
	PyExpression base class.
	"""

	__depends: List[str]

	@abstractmethod
	def __init__(self, expression: expr):
		"""
		Constructor for the expression.
		"""

	@abstractmethod
	def transpile(self) -> str:
		"""
		Transpiles this expression to a C++ string.
		"""

	def add_dependencies(self, dependencies: List[str]) -> None:
		"""
		Adds multiple dependencies to the dependency list.

		@param dependencies: A list of native dependencies that this object relies on.
		"""
		self.__depends.extend(dependencies)

	def add_dependency(self, dependency: str) -> None:
		"""
		Adds a single dependency to the list.

		@param dependency: The dependency to add.
		"""
		self.__depends.append(dependency)

	@staticmethod
	def from_expr(expression: expr) -> "PyExpression":
		"""
		Converts an AST expression to a PyExpression object.

		@param expression: The expression to convert.
		@return: A PyExpression object of the matching type.
		"""
		# Local import to avoid circular import errors
		from Constants import AST_EXPR_TO_PYEXPR

		# Get the expression type
		expr_type = type(expression)

		# If the expression is valid
		if expr_type in AST_EXPR_TO_PYEXPR:
			# Convert to PyExpression and return
			return AST_EXPR_TO_PYEXPR[type(expression)](expression)
		# Otherwise, it is probably a feature we do not support
		else:
			raise UnsupportedFeatureException(
				f"Python feature '{expr_type.__name__}' is not supported by the compiler.")
