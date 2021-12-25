"""
Compiler class for managing variables and their types between scopes.
"""
from src.Builtins import builtin_names
from src.Errors import VariableAlreadyDefinedError, VariableNotDefinedError
from src.Names import Value, Variable, Name, Function


class VarHandler:
	"""
	Handler for variables.
	"""

	__vars: dict[str, Name]

	def __init__(self):
		# Initialize the handler with builtin_names
		self.__vars = builtin_names

	def is_var_exists(self, var_name: str) -> bool:
		"""
		Returns boolean for if the specified variable name exists already.
		:param var_name: The name of the variable to check.
		"""
		return any(iter_var_name == var_name for iter_var_name in self.__vars)

	def init_var(self, var_name: str, var_type: str, initial_value: Value) -> Variable:
		"""
		Initialize a variable and add it to the handler registry.
		:param var_name: The name of the variable.
		:param var_type: The type of the variable.
		:param initial_value: The value that the variable starts with.
		"""
		# If variable does not exist
		if not self.is_var_exists(var_name):
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
			raise VariableAlreadyDefinedError(
				f"You cannot redefine variable '{var_name}' as it is already initialized.")

	def get_var(self, var_name: str) -> Name:
		"""
		Retreives the variable from the manager.
		:param var_name: The name of the variable.
		"""
		if self.is_var_exists(var_name):
			return self.__vars[var_name]
		else:
			raise VariableNotDefinedError(f"Variable '{var_name}' was not initialized yet.")

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
				# Cast it to a function
				obj: Function
				# Add it to the list
				func_list.append(obj)
		# Return the list
		return func_list
