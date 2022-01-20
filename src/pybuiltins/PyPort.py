"""
Port a native function or object to Python.
"""
from abc import ABCMeta, abstractmethod
from typing import Set, Union


class PyPort(metaclass=ABCMeta):
	"""
	Port a native object or object to Python.

	Technically this does no porting at all, and is quite the opposite-
	Porting only allows the compiler how to link between the Python
	objects and functions that call these ported objects.

	The transpiler will take this native defenition and bake it
	directly into the outputted transpilation. However, the important
	part of this process is that the transpiler will also remember this
	object for later usage (if necessary).
	"""

	__depends: Set[str]

	@abstractmethod
	def __init__(self, dependencies: Union[Set[str], None] = None) -> None:
		"""
		@param dependencies: A list of dependencies to require.
		"""
		# If default value
		if dependencies is None:
			# Set default value
			dependencies = set()

		# Initialize dependencies
		self.__depends = dependencies

	def get_dependencies(self) -> Set[str]:
		"""
		Returns the list of dependencies that this expression relies on.
		"""
		return self.__depends
