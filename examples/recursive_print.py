"""
Print a string forever, recursively.
"""


def loop_print(my_string: str, index: int) -> None:
    """
    Print a string, then recurse.
    Should print:

    [my_string]1
    [my_string]2
    [my_string]3
    ...

    :param index: The current looping index.
    :param my_string: The string to print.
    """
    print(my_string + str(index))
    loop_print(my_string, index + 1)


# Should cause a StackOverflow
# due to excessive recursion...
loop_print("test", 0)
