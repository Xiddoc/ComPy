"""
Compiler class for managing variables and their types between scopes.
"""
from typing import Set

from src.scopes.Object import Object
from src.structures.Errors import VariableAlreadyDefinedError, VariableNotDefinedError


class Scope:
	"""
	Handler for variables.
	"""

	__objects: Set[Object]

	def __init__(self) -> None:
		# TODO Initialize the handler with builtin_names
		self.__objects = set()

	def does_object_exist(self, object_name: str) -> bool:
		"""
		Returns True if the specified object name already exists.

		:param object_name: The name of the object to check.
		"""
		return any(iter_var.name == object_name for iter_var in self.__objects)

	# def declare_var(self, var_name: str, var_type: str) -> Variable:
	# 	"""
	# 	Initialize a variable and add it to the handler registry.
	#
	# 	:param var_name: The name of the variable.
	# 	:param var_type: The type of the variable.
	# 	:param initial_value: The value that the variable starts with.
	# 	"""
	# 	# If variable does not exist
	# 	if not self.does_object_exist(var_name):
	# 		# Make a new Variable
	# 		var = Variable(
	# 			var_name=var_name,
	# 			var_type=var_type,
	# 			initial_value=initial_value
	# 		)
	# 		# Append it to the variable list
	# 		self.__objects[var_name] = var
	# 		# Return it
	# 		return var
	# 	else:
	# 		# Otherwise, raise an exception (all variables have immutable types)
	# 		raise VariableAlreadyDefinedError(var_name)

	def get_object(self, object_name: str) -> Object:
		"""
		Retreives the object from the manager.
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
			raise VariableNotDefinedError(object_name)
