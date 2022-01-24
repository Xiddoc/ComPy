"""
Compiler class for managing variables and their types between scopes.
"""
from typing import Set, Optional

from src.scopes.Object import Object
from src.scopes.Variable import Variable
from src.structures.Errors import VariableAlreadyDefinedError, VariableNotDefinedError
from src.structures.TypeRenames import GENERIC_PYEXPR_TYPE


class Scope:
	"""
	Handler for variables.
	"""

	__objects: Set[Object]

	def __init__(self, parent: Optional[GENERIC_PYEXPR_TYPE] = None) -> None:
		# Import locally to avoid import error
		from src.pyexpressions.PyExpression import PyExpression
		# If a parent was passed
		# and the parent is a PyExpression
		if parent is not None and isinstance(parent, PyExpression):
			# Set the scope to the parent's scope
			self.__objects = parent.get_scope().get_objects()
		else:
			# TODO Initialize the handler with builtin_names
			self.__objects = set()

	def does_object_exist(self, object_name: str) -> bool:
		"""
		Returns True if the specified object name already exists.

		:param object_name: The name of the object to check.
		"""
		return any(iter_var == object_name for iter_var in self.__objects)

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
			self.__objects.add(Variable(name=var_name, type=var_type))
		else:
			# Otherwise, raise an exception.
			# All variables have immutable types, and
			# currently we do not support freeing objects.
			raise VariableAlreadyDefinedError(var_name)

	def get_object(self, object_name: str) -> Object:
		"""
		Retrieves the object from the manager.
		Throws an error if it doesn't exist.

		:param object_name: The name of the object to retrieve.
		"""
		# For each object
		for obj in self.__objects:
			# If the variable has this name
			if obj == object_name:
				# Return this variable
				return obj
		else:
			# Otherwise, if no variables were found
			raise VariableNotDefinedError(object_name)

	def get_objects(self) -> Set[Object]:
		"""
		Retrieves the full list of objects in the scope,
		and returns it.
		"""
		# Copy the set to a new set (use Python builtin methods for speed).
		# Basically a copy-by-value, so the external scope can't be altered.
		return set(list(self.__objects))
