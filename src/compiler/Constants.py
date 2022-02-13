"""
Constants and other 'singleton' objects and maps/dicts.
"""
from _ast import Constant, BinOp, operator, Add, Sub, Mult, AnnAssign, AST, Expr, Name, Call, FunctionDef, arg, \
	Return, Assign, Module, IfExp, If, cmpop, Eq, Compare, Lt, Gt, BoolOp, NotEq, Or, And, boolop, Div, Mod, FloorDiv
from json import dumps
from typing import Dict, Type, Any, Callable

from src.pyexpressions.abstract.PyExpression import PyExpression
from src.pyexpressions.concrete.PyAnnAssign import PyAnnAssign
from src.pyexpressions.concrete.PyArg import PyArg
from src.pyexpressions.concrete.PyAssign import PyAssign
from src.pyexpressions.concrete.PyBinOp import PyBinOp
from src.pyexpressions.concrete.PyBoolOp import PyBoolOp
from src.pyexpressions.concrete.PyCall import PyCall
from src.pyexpressions.concrete.PyCompare import PyCompare
from src.pyexpressions.concrete.PyConstant import PyConstant
from src.pyexpressions.concrete.PyExpr import PyExpr
from src.pyexpressions.concrete.PyFunctionDef import PyFunctionDef
from src.pyexpressions.concrete.PyIf import PyIf
from src.pyexpressions.concrete.PyIfExp import PyIfExp
from src.pyexpressions.concrete.PyModule import PyModule
from src.pyexpressions.concrete.PyName import PyName
from src.pyexpressions.concrete.PyReturn import PyReturn

AST_EXPR_TO_PYEXPR: Dict[Type[AST], Type[PyExpression]] = {
	AnnAssign: PyAnnAssign,
	Assign: PyAssign,
	arg: PyArg,
	BinOp: PyBinOp,
	BoolOp: PyBoolOp,
	Call: PyCall,
	Compare: PyCompare,
	Constant: PyConstant,
	Expr: PyExpr,
	FunctionDef: PyFunctionDef,
	If: PyIf,
	IfExp: PyIfExp,
	Module: PyModule,
	Name: PyName,
	Return: PyReturn,
}

AST_OP_TO_STR: Dict[Type[operator], str] = {
	Add: "+",
	Sub: "-",
	Mult: "*",
	Div: "/",
	FloorDiv: "//",
	Mod: "%"
}

AST_COMPARATOR_TO_STR: Dict[Type[cmpop], str] = {
	Eq: "==",
	NotEq: "!=",
	Lt: "<",
	Gt: ">"
}

AST_BOOLOP_TO_STR: Dict[Type[boolop], str] = {
	Or: "||",
	And: "&&"
}

PY_SPECIAL_CHARS: Dict[str, str] = {
	"\r": "\\r",
	"\n": "\\n",
	"\t": "\\t",
	"\b": "\\b"
}

PY_CONSTANT_CONVERSION_FUNC: Dict[Any, Callable[[Any], str]] = {
	int: str,
	bool: str,
	str: dumps,
	None: lambda _: "null"
}

PY_TYPES_TO_NATIVE_TYPES: Dict[str, str] = {
	"int": "int",
	"bool": "bool",
	"str": "std::string",
	"None": "null",
	"Any": "auto"
}
