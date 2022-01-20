"""
Variable class and other classes to represent values.
"""
from dataclasses import dataclass, field
from typing import Union, Optional


class Value:
	"""
	Dataclass for value.
	"""
	__value: Optional[str]
	__has_value: bool

	def __init__(self, value: Optional[str] = None) -> None:
		# If value given is null, then there is no starting value
		self.__has_value = value is not None
		self.__value = value

	def has_value(self) -> bool:
		"""
		Returns whether or not there is a value.
		"""
		return self.__has_value

	def get_value(self) -> str:
		"""
		Returns the TRANSPILED value.
		"""
		return "(" + "null" if self.__value is None else self.__value + ")"


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

	def get_init(self) -> str:
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

	def get_init(self) -> str:
		"""
		Transpiles the code for the initialization of the function.
		"""
		return f"{self.var_type} {self.var_name}{self.get_args()}{self.get_block()}"

	def get_args(self) -> str:
		"""
		Returns the argument list formatted into it's block.
		For example: (int test_one, char test_two)
		"""
		return f"({','.join(f'{arg.var_type} {arg.var_name}' for arg in self.arguments)})"

	def get_block(self) -> str:
		"""
		Returns the code block formatted in it's block.
		For example: {test(1);}
		"""
		return "{" + self.func_body + "}"

	def get_dependencies(self) -> list[str]:
		"""
		Returns the list of dependencies for this function.
		"""
		return self.dependencies


