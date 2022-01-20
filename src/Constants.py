"""
Constants and other 'singleton' objects and maps/dicts.
"""
from _ast import Constant, BinOp, operator, Add, Sub, Mult, AnnAssign, AST, Expr, Name, Call, FunctionDef, arg, Return
from typing import Dict, Type, Union

from src.pybuiltins.PyPort import PyPort
from src.pyexpressions.PyAnnAssign import PyAnnAssign
from src.pyexpressions.PyArg import PyArg
from src.pyexpressions.PyBinOp import PyBinOp
from src.pyexpressions.PyCall import PyCall
from src.pyexpressions.PyConstant import PyConstant
from src.pyexpressions.PyExpr import PyExpr
from src.pyexpressions.PyExpression import PyExpression
from src.pyexpressions.PyFunctionDef import PyFunctionDef
from src.pyexpressions.PyName import PyName
from src.pyexpressions.PyReturn import PyReturn

AST_EXPR_TO_PYEXPR: Dict[Type[AST], Type[PyExpression]] = {
	AnnAssign: PyAnnAssign,
	arg: PyArg,
	BinOp: PyBinOp,
	Call: PyCall,
	Constant: PyConstant,
	Expr: PyExpr,
	FunctionDef: PyFunctionDef,
	Name: PyName,
	Return: PyReturn,
}

AST_OP_TO_STR: Dict[Type[operator], str] = {
	Add: "+",
	Sub: "-",
	Mult: "*"
}

GENERIC_PYEXPR_TYPE = Union[Type[PyExpression], PyExpression, PyPort]
