"""
Variable class and other classes to represent values.
"""
from dataclasses import dataclass, field
from typing import Union


class Value:
	"""
	Dataclass for value.
	"""
	__value: Union[str, None]
	__has_value: bool

	def __init__(self, value: str = None):
		# If value given is null, then there is no starting value
		self.__has_value = not not value
		self.__value = value

	def has_value(self):
		"""
		Returns whether or not there is a value.
		"""
		return self.__has_value

	def get_value(self):
		"""
		Returns the TRANSPILED value.
		"""
		return "(" + self.__value + ")"


@dataclass
class Name:
	"""
	Dataclass for any name (object).
	"""
	var_name: str
	var_type: str


@dataclass
class Variable(Name):
	"""
	Dataclass for a variable.
	"""
	initial_value: Value

	def get_init(self):
		"""
		Transpiles the code for the initialization of the variable.
		"""
		return f"{self.var_type} {self.var_name} = {self.initial_value.get_value()};" \
			if self.initial_value.has_value() else \
			f"{self.var_type} {self.var_name};"


@dataclass
class Function(Name):
	"""
	Dataclass for a function.

	var_name: The name of the function.
	var_type: The return type of the function.
	"""
	arguments: list[Name] = field(default_factory=lambda: [])
	func_body: str = ""
	dependencies: list[str] = field(default_factory=lambda: [])

	def get_init(self):
		"""
		Transpiles the code for the initialization of the function.
		"""
		return f"{self.var_type} {self.var_name}{self.get_args()}{self.get_block()}"

	def get_args(self):
		"""
		Returns the argument list formatted into it's block.
		For example: (int test_one, char test_two)
		"""
		return f"({','.join(f'{arg.var_type} {arg.var_name}' for arg in self.arguments)})"

	def get_block(self):
		"""
		Returns the code block formatted in it's block.
		For example: {test(1);}
		"""
		return "{" + self.func_body + "}"

	def get_dependencies(self):
		"""
		Returns the list of dependencies for this function.
		"""
		return self.dependencies
