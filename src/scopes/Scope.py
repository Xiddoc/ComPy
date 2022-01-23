"""
Compiler class for managing variables and their types between scopes.
"""
from src.scopes.Names import Value, Variable, Name, Function
from src.structures.Errors import VariableAlreadyDefinedError, VariableNotDefinedError


class Scope:
	"""
	Handler for variables.
	"""

	__vars: dict[str, Name]

	def __init__(self) -> None:
		# Initialize the handler with builtin_names
		self.__vars = {}

	def does_var_exist(self, var_name: str) -> bool:
		"""
		Returns boolean for if the specified variable name exists already.

		:param var_name: The name of the variable to check.
		"""
		return any(iter_var_name == var_name for iter_var_name in self.__vars)

	def declare_var(self, var_name: str, var_type: str, initial_value: Value) -> Variable:
		"""
		Initialize a variable and add it to the handler registry.

		:param var_name: The name of the variable.
		:param var_type: The type of the variable.
		:param initial_value: The value that the variable starts with.
		"""
		# If variable does not exist
		if not self.does_var_exist(var_name):
			# Make a new Variable
			var = Variable(
				var_name=var_name,
				var_type=var_type,
				initial_value=initial_value
			)
			# Append it to the variable list
			self.__vars[var_name] = var
			# Return it
			return var
		else:
			# Otherwise, raise an exception (all variables have immutable types)
			raise VariableAlreadyDefinedError(var_name)

	def get_var(self, var_name: str) -> Name:
		"""
		Retreives the variable from the manager.
		:param var_name: The name of the variable.
		"""
		if self.does_var_exist(var_name):
			return self.__vars[var_name]
		else:
			raise VariableNotDefinedError(var_name)

	def get_funcs(self) -> list[Function]:
		"""
		Returns a list of all the functions loaded to the handler.
		"""
		# Init list
		func_list: list[Function] = []
		# For each name / object
		for obj in self.__vars.values():
			# If the object is a function
			if type(obj) == Function:
				# Add it to the list
				# noinspection PyTypeChecker
				func_list.append(obj)
		# Return the list
		return func_list
