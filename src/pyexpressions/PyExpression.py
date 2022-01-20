"""
PyExpression base class.
Used in extending for other pyexpressions.
"""
from _ast import AST
from abc import abstractmethod, ABCMeta
from typing import Set, Iterable

from src.Errors import UnsupportedFeatureException
from src.pybuiltins.PyPortFunction import PyPortFunction


class PyExpression(metaclass=ABCMeta):
	"""
	PyExpression base class.
	"""

	__expression: AST
	__depends: Set[str]
	__native_depends: Set["PyPortFunction"]

	@abstractmethod
	def __init__(self, expression: AST):
		"""
		Constructor for the expression.
		"""
		# Set base expression (might be needed later for throwing errors, will be useful for getting line #)
		self.__expression = expression
		# Create depenency sets
		self.__depends = set()
		self.__native_depends = set()

	@abstractmethod
	def transpile(self) -> str:
		"""
		Transpiles this expression to a C++ string.
		"""

	def add_dependencies(self, dependencies: Iterable[str]) -> None:
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

	def add_native_dependencies(self, native_dependencies: Iterable["PyPortFunction"]) -> None:
		"""
		Adds multiple native dependencies to the dependency list.

		@param native_dependencies: A list of native dependencies that this object relies on.
		"""
		self.__native_depends.update(native_dependencies)

	def add_native_dependency(self, native_dependency: "PyPortFunction") -> None:
		"""
		Adds a single native dependency to the list.

		@param native_dependency: The native dependency to add.
		"""
		self.__native_depends.add(native_dependency)

	def get_native_dependencies(self) -> Set["PyPortFunction"]:
		"""
		Returns the list of native (ported) dependencies that this expression relies on.
		"""
		return self.__native_depends

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
		# Inherit / extend dependencies to this object
		self.add_dependencies(obj.get_dependencies())
		self.add_native_dependencies(obj.get_native_dependencies())
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