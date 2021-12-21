"""
Compiler class.
"""
from argparse import Namespace
from ast import Module, AnnAssign, Name, Constant, expr, BinOp, operator, Add, Sub, Div, Mult, AST, parse, Expr, Call

from DependencyManager import DependencyManager
from Errors import UnsupportedFeatureException, VariableNotDefinedError
from Names import Value
from Output import Output
from VarHandler import VarHandler
from expressions.PyConstant import PyConstant
from expressions.PyExpression import PyExpression


class Compiler:
	"""
	Compiler class to convert operations to ASM ops.
	"""

	__node: AST
	__args: Namespace
	__output: Output
	__var_handler: VarHandler
	__dependency_manager: DependencyManager

	def __init__(self, args: Namespace):
		# Initialize the parser with the inputted parser instance
		self.__op_to_str: dict[type, str] = {Add: "+", Sub: "-", Div: "/", Mult: "*"}
		# Use the given arguments
		self.__args = args

	def compile(self, source: str) -> None:
		"""
		Entry to compilation sequence.
		"""
		# Initialize an empty dictionary for variables
		self.__var_handler = VarHandler()
		# Initialize the dependency manager
		self.__dependency_manager = DependencyManager()
		# Initialize segment for code
		self.__init_output()
		# Parse the node into an abstract tree
		self.__node = parse(source, self.__args.file.name)

		# Walk down the node
		for node in self.__node.body:
			# Get the type of the node
			node_type = type(node)

			print(node)

			# Switch-like statement (if/elif) for matching node type
			# If multiline comment (Python literal string which is not assigned to a variable)
			if node_type == Module:
				# Do something later if necessary with imports
				continue

			# Type defenition
			# elif node_type == AnnAssign:
			# 	# Initialize the varaible in the manager
			# 	var = self.__var_handler.init_var(
			# 		var_name=node.target.id,
			# 		var_type=node.annotation.id,
			# 		initial_value=self.eval_expr(node.value)
			# 	)
			# 	# Write to header
			# 	self.__output.code(var.get_init())
			#
			# # Name (variable) usage
			# elif node_type == Name:
			# 	# Verify that name has been initialized
			# 	# If it is not
			# 	if not self.__var_handler.is_var_exists(node.id):
			# 		# Raise an error
			# 		raise VariableNotDefinedError(f"Variable '{node.id}' has was not initialized before usage.")

			# Base expression (function, literal string comment / mutliline comment)
			elif node_type == Expr:
				# Make sure
				# Evaluate the expression
				# Write it to the code segment
				self.__output.write(self.eval_expr(node.value))

			else:
				# If the compiler could not understand the operation
				# Then throw an unsupported operation error
				raise UnsupportedFeatureException(
					f"Python feature '{node_type.__name__}' is not supported by the compiler.")

		# Complete by injecting headers
		# self.__output.header(self.__dependency_manager.format_dependencies())

	def eval_expr(self, expression: expr) -> PyExpression:
		"""
		Takes an expression and evaluates it to code.
		:param expression: AST expression class or class that extends it.
		"""
		# Get the type of the constant
		expr_type = type(expression)

		# If value is a constant
		if expr_type == Constant:
			# Transpile the constant
			# Return the constant
			expression: Constant
			return PyConstant(expression)

		# elif expr_type == BinOp:
		# 	# If value is a binary operation
		# 	# Then evaluate the operation
		# 	return self.eval_op(expression.left, expression.op, expression.right)
		#
		# elif expr_type == Name:
		# 	# If the value is a name (variable)
		# 	# Then return the variable name
		# 	return Value(self.__var_handler.get_var(expression.id).var_name)
		#
		# elif expr_type == Call:
		# 	# If value is an expression (function, literals)
		# 	return Value(f"{expression.func.id}({','.join(self.eval_expr(arg).get_value() for arg in expression.args)})")

		# Guess we can not do anything :(
		raise UnsupportedFeatureException(f"Python feature '{expr_type.__name__}' is not supported by the compiler.")

	def eval_op(self, left: expr, op: operator, right: expr) -> Value:
		"""
		Evaluates (transpiles) an operation.
		:param left: The left side of the operation.
		:param op: The operation given.
		:param right: The right side of the operation.
		:return: A string representing the transpiled version of the operation.
		"""
		# Transpile operation
		return Value(self.eval_expr(left).get_value() + self.__op_to_str[type(op)] + self.eval_expr(right).get_value())

	def get_output(self) -> str:
		"""
		Returns the compiled output as a string.
		"""
		return self.__output.get_output()

	def __init_output(self) -> None:
		"""
		Initialize the output dictionary structure.
		"""
		# Init output handler
		self.__output = Output()
		# Write defaults to sections
		# self.__output.code("int main() {")
		# self.__output.footer("return 0; }")
		# # Implement builtins
		# for func in self.__var_handler.get_funcs():
		# 	# Write init of func
		# 	self.__output.func(func.get_init())
		# 	# Add dependencies
		# 	self.__dependency_manager.add_dependencies(func.get_dependencies())
