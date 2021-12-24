"""
Python Builtin functions and types.
"""
from src.Names import Value, Variable, Function, Name

builtin_names: dict[str, Name] = {
	"int": Variable("int", "type", Value()),
	"str": Variable("str", "type", Value()),
	"print": Function("print", "void", [Name("value", "auto")], 'std::cout<<value<<std::endl;', ["iostream"])
	# "input": Function("input", "std::string", [])
}

