"""
Constants and other 'singleton' objects and maps/dicts.
"""
from _ast import Constant, BinOp, operator, Add, Sub, Mult, AnnAssign, AST
from typing import Dict, Type

from expressions.PyAnnAssign import PyAnnAssign
from expressions.PyBinOp import PyBinOp
from expressions.PyConstant import PyConstant
from expressions.PyExpression import PyExpression

AST_EXPR_TO_PYEXPR: Dict[Type[AST], Type[PyExpression]] = {
	Constant: PyConstant,
	BinOp: PyBinOp,
	AnnAssign: PyAnnAssign
}

AST_OP_TO_STR: Dict[Type[operator], str] = {
	Add: "+",
	Sub: "-",
	Mult: "*"
}
