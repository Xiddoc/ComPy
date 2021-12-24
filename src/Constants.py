"""
Constants and other 'singleton' objects and maps/dicts.
"""
from _ast import Constant, BinOp, operator, Add, Sub, Mult, AnnAssign, AST, Expr, Name, Call, FunctionDef, arg, Return
from typing import Dict, Type

from src.expressions.PyAnnAssign import PyAnnAssign
from src.expressions.PyArg import PyArg
from src.expressions.PyBinOp import PyBinOp
from src.expressions.PyCall import PyCall
from src.expressions.PyConstant import PyConstant
from src.expressions.PyExpr import PyExpr
from src.expressions.PyExpression import PyExpression
from src.expressions.PyFunctionDef import PyFunctionDef
from src.expressions.PyName import PyName
from src.expressions.PyReturn import PyReturn

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
