"""
Class defenition.
"""
from _ast import ClassDef
from typing import List, Optional

from src.compiler.Util import Util
from src.pyexpressions.abstract.PyExpression import PyExpression
from src.pyexpressions.concrete.PyAnnAssign import PyAnnAssign
from src.pyexpressions.concrete.PyFunctionDef import PyFunctionDef
from src.pyexpressions.highlevel.PyIdentifiable import PyIdentifiable
from src.pyexpressions.highlevel.PyScoped import PyScoped
from src.scopes.objects.Class import Class
from src.structures.Errors import UnsupportedFeatureException
from src.structures.TypeRenames import GENERIC_PYEXPR_TYPE


class PyClassDef(PyScoped, PyIdentifiable):
    """
    Class defenition.
    """

    __constructor: Optional[PyFunctionDef]
    __private_methods: List[PyFunctionDef]
    __public_methods: List[PyFunctionDef]
    __private_fields: List[PyAnnAssign]
    __public_fields: List[PyAnnAssign]

    def __init__(self, expression: ClassDef, parent: GENERIC_PYEXPR_TYPE):
        super().__init__(expression, parent)

        # Store class name
        self.set_id(expression.name)

        # Declare class
        self.get_nearest_scope().declare_object(Class(self.get_id()))

        # Create object scope (class body has it's own scope)
        # Inherit the scope from the previous scope
        self.update_from_nearest_scope()

        # Prepare to store methods and fields
        self.__constructor = None
        self.__private_fields = []
        self.__public_fields = []
        self.__private_methods = []
        self.__public_methods = []
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

            # If the expression's name starts with 2 underscores,
            # then Python will mangle the name, hence "making it private"
            # (it's not exactly private, since you can still access it, but
            # it's the best way to use encapsulation in Python).

            # If the expression is an assignment
            elif isinstance(pyexpr, PyAnnAssign):
                # Add it to the fields
                if pyexpr.get_id().startswith("__"):
                    # Private field
                    self.__private_fields.append(pyexpr)
                else:
                    # Public field
                    self.__public_fields.append(pyexpr)

            # If the expression is a function definition
            elif isinstance(pyexpr, PyFunctionDef):
                # Then it is a function method (class function)
                # Check if it is the constructor
                if pyexpr.get_id() == "__init__":
                    # Constructor
                    self.__constructor = pyexpr
                elif pyexpr.get_id().startswith("__"):
                    # Private method
                    self.__private_methods.append(pyexpr)
                else:
                    # Public method
                    self.__public_methods.append(pyexpr)

            # Not sure what this is, but it can't be in the external body of the class
            else:
                raise UnsupportedFeatureException(f"{Util.get_name(expr)} in class body")

    def transpile_constructor(self) -> str:
        """
        Transpiles the class constructor, if there is one.
        """
        return "" if self.__constructor is None else \
            f"{self.get_id()}({self.__constructor.transpile_args()}) {self.__constructor.transpile_code()};"

    # noinspection PyUnusedFunction
    def _transpile(self) -> str:
        """
        Transpile the statement to a string.
        """
        # Class header
        transpiled_class = [f"class {self.get_id()} {{"]

        # If there are any private attributes
        if self.__private_methods or self.__private_fields:
            # Then mark this section as private
            transpiled_class.append("private:")
            # Add transpiled private fields and methods
            if self.__private_fields:
                transpiled_class.append("\n".join([pyexpr.transpile() + ";" for pyexpr in self.__private_fields]))
            if self.__private_methods:
                transpiled_class.append("\n".join([pyexpr.transpile() + ";" for pyexpr in self.__private_methods]))

        # If there are any public attributes (or a constructor)
        if self.__constructor or self.__public_methods or self.__public_fields:
            # Then mark this section as public
            transpiled_class.append("public:")
            # Transpile and add public attributes
            if self.__public_fields:
                transpiled_class.append("\n".join([pyexpr.transpile() + ";" for pyexpr in self.__public_fields]))
            if self.__constructor:
                transpiled_class.append(self.transpile_constructor())
            if self.__public_methods:
                transpiled_class.append("\n".join([pyexpr.transpile() + ";" for pyexpr in self.__public_methods]))

        # Add ending bracket
        transpiled_class.append("}")
        # Join transpiled segments together
        return "\n".join(transpiled_class)
