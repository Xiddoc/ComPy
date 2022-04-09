"""
Constants and other 'singleton' objects and maps/dicts.
"""
from _ast import Constant, BinOp, operator, Add, Sub, Mult, AnnAssign, AST, Expr, Name, Call, FunctionDef, arg, \
    Return, Assign, Module, IfExp, If, cmpop, Eq, Compare, Lt, Gt, BoolOp, NotEq, Or, And, boolop, Div, Mod, FloorDiv, \
    Pass, GtE, LtE, While, AugAssign, Break, For, ClassDef, Attribute
from json import dumps
from typing import Dict, Type, Any, Callable

from src.pyexpressions.abstract.PyExpression import PyExpression
from src.pyexpressions.concrete.PyAnnAssign import PyAnnAssign
from src.pyexpressions.concrete.PyArg import PyArg
from src.pyexpressions.concrete.PyAssign import PyAssign
from src.pyexpressions.concrete.PyAttribute import PyAttribute
from src.pyexpressions.concrete.PyAugAssign import PyAugAssign
from src.pyexpressions.concrete.PyBinOp import PyBinOp
from src.pyexpressions.concrete.PyBoolOp import PyBoolOp
from src.pyexpressions.concrete.PyBreak import PyBreak
from src.pyexpressions.concrete.PyCall import PyCall
from src.pyexpressions.concrete.PyClassDef import PyClassDef
from src.pyexpressions.concrete.PyCompare import PyCompare
from src.pyexpressions.concrete.PyConstant import PyConstant
from src.pyexpressions.concrete.PyExpr import PyExpr
from src.pyexpressions.concrete.PyFor import PyFor
from src.pyexpressions.concrete.PyFunctionDef import PyFunctionDef
from src.pyexpressions.concrete.PyIf import PyIf
from src.pyexpressions.concrete.PyIfExp import PyIfExp
from src.pyexpressions.concrete.PyModule import PyModule
from src.pyexpressions.concrete.PyName import PyName
from src.pyexpressions.concrete.PyPass import PyPass
from src.pyexpressions.concrete.PyReturn import PyReturn
from src.pyexpressions.concrete.PyWhile import PyWhile

AST_EXPR_TO_PYEXPR: Dict[Type[AST], Type[PyExpression]] = {
    AnnAssign: PyAnnAssign,
    Assign: PyAssign,
    Attribute: PyAttribute,
    AugAssign: PyAugAssign,
    arg: PyArg,
    BinOp: PyBinOp,
    BoolOp: PyBoolOp,
    Break: PyBreak,
    Call: PyCall,
    ClassDef: PyClassDef,
    Compare: PyCompare,
    Constant: PyConstant,
    Expr: PyExpr,
    For: PyFor,
    FunctionDef: PyFunctionDef,
    If: PyIf,
    IfExp: PyIfExp,
    Module: PyModule,
    Name: PyName,
    Pass: PyPass,
    Return: PyReturn,
    While: PyWhile,
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
    LtE: "<=",
    Gt: ">",
    GtE: ">="
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

PY_CONSTANT_CONVERSION_FUNC: Dict[str, Callable[[Any], str]] = {
    "int": str,
    "bool": str,
    "str": dumps,
    "NoneType": lambda _: "null"
}

PY_TYPES_TO_NATIVE_TYPES: Dict[str, str] = {
    "int": "int",
    "bool": "bool",
    "str": "std::string",
    "None": "null",
    "Any": "auto"
}

OUTPUT_CODE_TEMPLATE: str = """
{dependency_code}

{ported_headers}

{ported_code}

{transpiled_funcs}

int main() {{
    /* Transpiled with ComPy */
    {transpiled_code}
    return 0;
}}
"""
