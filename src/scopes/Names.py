"""
Variable class and other classes to represent values.
"""
from dataclasses import dataclass, field


@dataclass
class Name:
	"""
	Dataclass for any name (object).
	"""
	var_name: str
	var_type: str


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


