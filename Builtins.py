"""
Python Builtin functions and types.
"""
from Names import Value, Variable, Function, Name

builtin_names: dict[str, Name] = {
	"int": Variable("int", "type", Value()),
	"str": Variable("str", "type", Value()),
	"print": Function("print", "void", [Name("value", "auto")], 'std::cout<<value;', ["iostream"])
}

escaped_python_strings = {
	"\\": "\\\\",
	"\n": "\\n",
	"\t": "\\t",
	"\r": "\\r",
	"\b": "\\b",
	"\'": "\\'",
	"\f": "\\f"
}
