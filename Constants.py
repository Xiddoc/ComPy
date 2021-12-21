"""
Constants and other 'singleton' objects and maps/dicts.
"""
from _ast import expr, Constant, BinOp, operator, Add, Sub, Mult
from typing import Dict, Type

from expressions.PyBinOp import PyBinOp
from expressions.PyConstant import PyConstant
from expressions.PyExpression import PyExpression

AST_EXPR_TO_PYEXPR: Dict[Type[expr], Type[PyExpression]] = {
	Constant: PyConstant,
	BinOp: PyBinOp
}

AST_OP_TO_STR: Dict[Type[operator], str] = {
	Add: "+",
	Sub: "-",
	Mult: "*"
}
