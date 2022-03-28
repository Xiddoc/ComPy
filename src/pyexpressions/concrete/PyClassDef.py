"""
Class defenition.
"""
from _ast import ClassDef
from typing import List

from src.pyexpressions.concrete.PyFunctionDef import PyFunctionDef
from src.pyexpressions.highlevel.PyScoped import PyScoped
from src.structures.TypeRenames import GENERIC_PYEXPR_TYPE


class PyClassDef(PyScoped):
    """
    Class defenition.
    """

    __class_name: str
    __methods: List[PyFunctionDef]

    def __init__(self, expression: ClassDef, parent: GENERIC_PYEXPR_TYPE):
        super().__init__(expression, parent)

        # Store class name
        self.__class_name = expression.name

        # Declare class
        # self.get_scope().declare_class

        # Create object scope (function body has it's own scope)
        # Inherit the scope from the previous scope
        # self.__scope = Scope(self.get_nearest_scope())

        # For each object in the body
        # We will have to assign each expression individually,
        # since unlike a Python class, C++ classes have an
        # organized structure (public, private, fields, etc.)
        # for expr in expression.body:
        #     # If the expression is an assignment
        #     if isinstance(expr, AnnAssign):
        #         self.__scope.declare_variable()
        #     else:
        #         # Not sure what this is, but it can't be in the external body of the class
        #         raise UnsupportedFeatureException(f"{expr} in class body")

    def get_class_name(self) -> str:
        """
        :return: The name of the referenced class.
        """
        return self.__class_name

    # noinspection PyUnusedFunction
    def _transpile(self) -> str:
        """
        Transpile the statement to a string.
        """
        return "/*class*/"

