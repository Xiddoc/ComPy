"""
Basic fibonacci algorithm example.
"""


def fib(index: int) -> int:
    """
    Calculate the fibonacci by index.

    :param index: The index to calculate to.
    :return: The fibonacci value at that index.
    """
    return index if index <= 1 else fib(index - 1) + fib(index - 2)


fib_index: int = 35
print("Calculating index " + str(fib_index) + " of fibonacci series...")
print(fib(fib_index))
