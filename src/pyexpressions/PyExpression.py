"""
PyExpression base class.
Used in extending for other pyexpressions.
"""
from _ast import AST
from abc import abstractmethod, ABCMeta
from typing import List, Set, Union

from src.Errors import UnsupportedFeatureException


# noinspection PyUnusedFunction
class PyExpression(metaclass=ABCMeta):
	"""
	PyExpression base class.
	"""

	__expression: AST
	__depends: Set[str]

	@abstractmethod
	def __init__(self, expression: AST):
		"""
		Constructor for the expression.
		"""
		# Set base expression
		self.__expression = expression
		# Create depenency set
		self.__depends = set()

	@abstractmethod
	def transpile(self) -> str:
		"""
		Transpiles this expression to a C++ string.
		"""

	def add_dependencies(self, dependencies: Union[Set[str], List[str]]) -> None:
		"""
		Adds multiple dependencies to the dependency list.

		@param dependencies: A list of native dependencies that this object relies on.
		"""
		self.__depends.update(dependencies)

	def add_dependency(self, dependency: str) -> None:
		"""
		Adds a single dependency to the list.

		@param dependency: The dependency to add.
		"""
		self.__depends.add(dependency)

	def get_dependencies(self) -> Set[str]:
		"""
		Returns the list of dependencies that this expression relies on.
		"""
		return self.__depends

	def get_expression(self) -> AST:
		"""
		@return: Returns the expression this instance is holding (was initialized with).
		"""
		return self.__expression

	def from_ast(self, expression: AST) -> "PyExpression":
		"""
		Converts an AST expression to a PyExpression object.

		As opposed to the static from_ast method, this one
		inherits dependencies directly to the current object.

		@param expression: The expression to convert.
		@return: A PyExpression object of the matching type.
		"""
		# Convert to PyExpression
		obj: PyExpression = PyExpression.from_ast_statically(expression)
		# Extend dependencies to this object
		self.add_dependencies(obj.get_dependencies())
		# Return new object
		return obj

	@staticmethod
	def from_ast_statically(expression: AST) -> "PyExpression":
		"""
		Converts an AST expression to a PyExpression object.

		@param expression: The expression to convert.
		@return: A PyExpression object of the matching type.
		"""
		# Local import to avoid circular import errors
		from src.Constants import AST_EXPR_TO_PYEXPR

		# Get the expression type
		expr_type = type(expression)

		# If the expression is valid
		if expr_type in AST_EXPR_TO_PYEXPR:
			# Convert to PyExpression and return
			return AST_EXPR_TO_PYEXPR[expr_type](expression)
		# Otherwise, it is probably a feature we do not support
		else:
			raise UnsupportedFeatureException(
				f"Python feature '{expr_type.__name__}' is not supported by the compiler.")
