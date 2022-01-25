"""
Compiler class.
"""
from ast import AST, parse, unparse
from functools import reduce
from typing import Any, Union

from src.compiler.Args import Args
from src.compiler.Output import Output
from src.pyexpressions.PyExpression import PyExpression
from src.pybuiltins.PyPortFunction import PyPortFunction


class Compiler:
	"""
	Compiler class to convert operations to ASM ops.
	"""

	__node: AST
	__output: Output

	def parse(self, source: str) -> None:
		"""
		Initiates the parsing sequence.
		This turns the code into a series of nodes, filled
		with the proper data structures alongside other nested nodes.
		"""
		# Init output handler
		self.__output = Output()
		# Parse the node into an abstract tree
		self.__node = parse(source, Args().get_args().file.name)

		# Walk down the node
		for node in self.__node.body:
			# Get the type of the node
			node_type = type(node)

			# Evaluate the expression
			# Write it to the code segment
			self.__output.write(PyExpression.from_ast_statically(node, None))

	def compile(self) -> str:
		"""
		Returns the compiled output as a string.
		"""
		return self.__output.compile_to_string()

	@staticmethod
	def get_attr(obj: Union[AST, "PyPortFunction"], attribute_path: str) -> Any:
		"""
		A function that recursively traverses down an "attribute path"
		and retrieves the value at the end of the path.

		This function exists since the CPython ast library uses an odd
		system which dynamically adds attributes to the AST instances,
		instead of statically declaring them in their respective classes.

		Due to this, mypy will throw a type-checking error since it will
		not find these attributes in the class defenition. Hence, to work
		around this bug, we will use the getattr function to retrieve the
		attributes directly.

		:param obj: The AST object to traverse.
		:param attribute_path: The attribute path to use (for example, if passing
								the object 'expression', and you want to navigate
								to the 'target' attribute, then the 'id' attribute
								of the 'target' attribute, then for this parameter
								you would pass the string "target.id").
		"""
		# Split by .
		# For example: "expression.target.id" becomes ["expression", "target", "id"]
		attrs = attribute_path.split(".")

		# Built in functools' reduce function to cumulatively execute the getattr function
		# On the first 2 arguments of the list
		return reduce(getattr, attrs, obj)

	@classmethod
	def get_name(cls, obj: Union[AST, "PyPortFunction"]) -> str:
		"""
		Retrieves the name of the AST node's class.
		For example, instead of seeing: <ast.AnnAssign object at 0x000002CC7FE5A310>
		You could use this method to abbreviate to: AnnAssign

		:param obj: An instance of the AST expression or node to name.
		:return: The string representation of the AST node's class name.
		"""
		return str(cls.get_attr(obj, "__class__.__name__"))

	@staticmethod
	def unparse(expression: AST) -> str:
		"""
		Takes an AST expression or node and unparses it back
		to Python code (or a Python expression, that is).

		:param expression: The AST node to unparse.
		:return: The Python representation of the node.
		"""
		return unparse(expression)

	@classmethod
	def unparse_escaped(cls, expression: AST) -> str:
		"""
		Takes an AST expression or node and unparses it back
		to Python code (or a Python expression, that is).
		Following that, it escapes all special characters
		so that it is now a printable literal where
		the special characters are not interpreted.

		:param expression: The AST node to unparse.
		:return: The *string-escaped* Python representation of the node.
		"""
		# Import locally to avoid cyclic import error
		from src.compiler.Constants import PY_SPECIAL_CHARS
		# First, unparse the expression
		unparsed_code: str = cls.unparse(expression)

		# For each special character
		for special_char, escaped_char in PY_SPECIAL_CHARS.items():
			# Replace with the escaped version
			unparsed_code = unparsed_code.replace(special_char, escaped_char)

		# Return the escaped string
		return unparsed_code
