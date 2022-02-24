"""
Compiler class for managing variables and their types between scopes.
"""
from typing import Set, Optional

from src.scopes.Object import Object
from src.scopes.Type import Type
from src.scopes.Variable import Variable
from src.structures.Errors import ObjectAlreadyDefinedError, ObjectNotDefinedError


class Scope:
	"""
	Handler for variables.
	"""

	__objects: Set[Object]

	def __init__(self, external_scope: Optional["Scope"] = None) -> None:
		if external_scope is not None:
			# Initiate the scope with the parent scope's objects
			self.__objects = external_scope.get_objects()
		else:
			# TODO Initialize the handler with builtin_names
			self.__objects = set()

	def does_object_exist(self, object_name: str) -> bool:
		"""
		Returns True if the specified object name already exists.

		:param object_name: The name of the object to check.
		"""
		return any(iter_var.name == object_name for iter_var in self.__objects)

	def declare_var(self, var_name: str, var_type: str) -> None:
		"""
		Initialize a variable and add it to the handler's registry.

		:param var_name: The name of the variable.
		:param var_type: The type of the variable.
		"""
		# If variable does not exist
		if not self.does_object_exist(var_name):
			# Make a new Variable
			# Add it to the object set
			self.__objects.add(Variable(name=var_name, type=Type(var_type)))
		else:
			# Otherwise, raise an exception.
			# All variables have immutable types, and
			# currently we do not support freeing objects.
			raise ObjectAlreadyDefinedError(var_name)

	def get_object(self, object_name: str) -> Object:
		"""
		Retrieves the object from the manager.
		Throws an error if it doesn't exist.

		:param object_name: The name of the object to retrieve.
		"""
		# For each object
		for obj in self.__objects:
			# If the variable has this name
			if obj.name == object_name:
				# Return this variable
				return obj
		else:
			# Otherwise, if no variables were found
			raise ObjectNotDefinedError(object_name)

	def get_objects(self) -> Set[Object]:
		"""
		Retrieves the full list of objects in the scope,
		and returns it.
		"""
		# Copy the set to a new set (use Python builtin methods for speed).
		# Basically a copy-by-value, so the external scope can't be altered.
		return set(list(self.__objects))
