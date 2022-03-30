"""
Class defenition.
"""
from _ast import ClassDef
from typing import List

from src.compiler.Util import Util
from src.pyexpressions.abstract.PyExpression import PyExpression
from src.pyexpressions.concrete.PyAnnAssign import PyAnnAssign
from src.pyexpressions.concrete.PyFunctionDef import PyFunctionDef
from src.pyexpressions.highlevel.PyScoped import PyScoped
from src.structures.Errors import UnsupportedFeatureException
from src.structures.TypeRenames import GENERIC_PYEXPR_TYPE


class PyClassDef(PyScoped):
    """
    Class defenition.
    """

    __class_name: str
    __methods: List[PyFunctionDef]
    __fields: List[PyAnnAssign]

    def __init__(self, expression: ClassDef, parent: GENERIC_PYEXPR_TYPE):
        super().__init__(expression, parent)

        # Store class name
        self.__class_name = expression.name

        # Declare class
        # self.get_scope().declare_class

        # Create object scope (function body has it's own scope)
        # Inherit the scope from the previous scope
        # self.__scope = Scope(self.get_nearest_scope())

        # Prepare to store methods and fields
        self.__fields = []
        self.__methods = []
        # For each object in the body
        # We will have to assign each expression individually,
        # since unlike a Python class, C++ classes have an
        # organized structure (public, private, fields, etc.)
        for expr in expression.body:
            # Parse the expression
            pyexpr: PyExpression = self.from_ast(expr)
            # If the expression is dead
            if pyexpr.is_dead_expression():
                # Then ignore it
                continue
            # If the expression is an assignment
            elif isinstance(pyexpr, PyAnnAssign):
                # Add it to the fields
                self.__fields.append(pyexpr)
            # If the expression is a function definition
            elif isinstance(pyexpr, PyFunctionDef):
                # Then it is a method, add it to the pack
                self.__methods.append(pyexpr)
            else:
                # Not sure what this is, but it can't be in the external body of the class
                raise UnsupportedFeatureException(f"{Util.get_name(expr)} in class body")

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
