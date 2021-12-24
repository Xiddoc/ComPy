"""
Constants and other 'singleton' objects and maps/dicts.
"""
from _ast import Constant, BinOp, operator, Add, Sub, Mult, AnnAssign, AST, Expr
from typing import Dict, Type

from src.expressions.PyAnnAssign import PyAnnAssign
from src.expressions.PyBinOp import PyBinOp
from src.expressions.PyConstant import PyConstant
from src.expressions.PyExpr import PyExpr
from src.expressions.PyExpression import PyExpression

AST_EXPR_TO_PYEXPR: Dict[Type[AST], Type[PyExpression]] = {
	Expr: PyExpr,
	Constant: PyConstant,
	BinOp: PyBinOp,
	AnnAssign: PyAnnAssign
}

AST_OP_TO_STR: Dict[Type[operator], str] = {
	Add: "+",
	Sub: "-",
	Mult: "*"
}
