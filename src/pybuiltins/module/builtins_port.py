"""
Native port for the Python builtin standard library.
"""
from typing import Dict, Any

from src.pybuiltins.PyPortFunctionSignature import PyPortFunctionSignature


# noinspection PyShadowingBuiltins,PyUnusedLocal
def range(end: int) -> Any:
    """
    Creates a range of numbers to iterate on.

    :param end: The final number to iterate to (starting from 0).
    """


# noinspection PyShadowingBuiltins,PyUnusedLocal
def print(print_string: Any) -> None:
    """
    Prints a string to standard output.

    :param print_string: The string to print.
    """


# noinspection PyUnusedLocal,PyShadowingBuiltins
def input(print_string: str) -> str:
    """
    Takes input from the user.

    :param print_string: A string to print before taking input.
    :return: The user input, until the user presses the Enter key.
    """


# noinspection PyUnusedLocal
def str_cast(obj: Any) -> str:
    """
    Casts any object to a string, if possible.

    :param obj: The object to cast.
    :return: The string version of this object.
    """


# noinspection PyUnusedLocal
def int_cast(obj: str) -> str:
    """
    Casts a string object to an integer.

    :param obj: The string to cast.
    :return: The integer representation of this string.
    """


# noinspection PyShadowingBuiltins,PyUnusedLocal
def pow(value: int, exponent: int) -> int:
    """
    Calculates a number to the power of the given exponent.

    :param value: The base value.
    :param exponent: The exponent's value.
    :return: The power of the base to the exponent.
    """


ported_objs: Dict[str, PyPortFunctionSignature] = {
    "range": PyPortFunctionSignature(
        function=range,
        code="class range {\npublic:\n\tclass iterator {\n\t\tfriend class range;\n\tpublic:\n\t\t// Must-have for "
             "iterator\n\t\tlong operator *() const { return index_; }\n\n\t\t// Called for each iteration\n\t\tconst "
             "iterator &operator ++() {\n\t\t\tindex_ += step_;\n\t\t\treturn *this;\n\t\t}\n\n\t\t// Called for each "
             "iteration\n\t\tbool operator !=(const iterator &other) const {\n\t\t\t// If this returns *false*, "
             "the loop will quit\n\t\t\t// IF the index is smaller than the end index\n\t\t\t// AND the \'end\' flag "
             "is not on\n\t\t\t// THEN return true, meaning that any\n\t\t\t// other case will return false (exit "
             "loop)\n\t\t\treturn !end_now_ && index_ < other.index_;\n\t\t}\n\n\tprotected:\n\t\texplicit iterator("
             "long start, long step = 0, bool end_now = false) : index_(start), end_now_(end_now), step_(step) { "
             "}\n\n\tprivate:\n\t\tlong index_;\n\t\tbool end_now_;\n\t\tlong step_;\n\t};\n\n\t// Iterator "
             "methods\n\titerator begin() const { return begin_; }\n\titerator end() const { return end_; }\n\n\t// "
             "Constructor\n\texplicit range(long begin, long end, long step = 1) : begin_(begin, step, (begin - end) > "
             "0 == step > 0), end_(end) {}\n\texplicit range(long end, long step = 1) : begin_(0, step, end < 0 == "
             "step > 0), end_(end) {}\nprivate:\n\titerator begin_;\n\titerator end_;\n};\nreturn range(end);"
    ),
    "print": PyPortFunctionSignature(
        function=print,
        code="std::cout<<print_string<<std::endl;",
        dependencies={"iostream"}
    ),
    "input": PyPortFunctionSignature(
        function=input,
        code="print(std::move(print_string));std::string s;std::cin>>s;return s;",
        dependencies={"iostream", "utility"},
        linked_ports={"print"}
    ),
    "str": PyPortFunctionSignature(
        function=str_cast,
        code="return std::to_string(obj);",
        dependencies={"iostream"}
    ),
    "int": PyPortFunctionSignature(
        function=int_cast,
        code="return std::stoi(obj);",
        dependencies={"iostream"}
    ),
    "pow": PyPortFunctionSignature(
        function=pow,
        code="return pow(value, exponent);",
        dependencies={"cmath"}
    )
}
