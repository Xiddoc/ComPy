"""
Class for a conditional looped statement.
"""
from _ast import For, AnnAssign, Name, Call
from typing import cast

from src.compiler.Util import Util
from src.pyexpressions.abstract.PyExpression import PyExpression
from src.pyexpressions.concrete.PyAnnAssign import PyAnnAssign
from src.pyexpressions.concrete.PyCall import PyCall
from src.pyexpressions.highlevel.PyBody import PyBody
from src.structures.TypeRenames import GENERIC_PYEXPR_TYPE


# Does not inherit from PyConditional as it
# does NOT have a 'test' attribute (condition).
# This is since in Python, all 'for' loops are
# actually just 'foreach' loops (iterate for
# each item in an Iterable).
class PyFor(PyExpression):
    """
    Class for a Python iterating statement (for statement).
    """

    __target: PyAnnAssign
    __iter: PyCall
    __code: PyBody

    def __init__(self, expression: For, parent: GENERIC_PYEXPR_TYPE) -> None:
        super().__init__(expression, parent)

        # Create and set iterator to field
        self.__target = PyAnnAssign(
            expression=AnnAssign(Name(Util.get_attr(expression.target, "id"), None), Name("Any", None), None, simple=1),
            parent=self
        )

        # Set iterable to field
        self.__iter = PyCall(cast(Call, expression.iter), self)

        # Create body, now that iterator exists
        self.__code = PyBody(Util.get_attr(expression, 'body'), parent)

    def _transpile(self) -> str:
        """
        Transpile the conditional statement to a string.
        """
        return f"for ({self.__target.transpile()} : {self.__iter.transpile()}) {self.__code.transpile()}"
