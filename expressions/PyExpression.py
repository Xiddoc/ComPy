"""
PyExpression base class.
Used in extending for other expressions.
"""
from abc import abstractmethod, ABCMeta
from typing import List


class PyExpression(metaclass=ABCMeta):
	"""
	PyExpression base class.
	"""

	__depends: List[str]

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