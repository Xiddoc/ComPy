"""
Print a string forever, recursively.
"""


def conditional_print(index: int) -> None:
    """
    Print a string, depending on the condition met.
    Should print:

    [my_string]1
    [my_string]2
    [my_string]3
    ...

    :param index: The current looping index.
    """

    print(index)

    if index == 0 and index != 2 or index != 3:
        print("Equals to 0!")
    elif 1 < 2 < index < 5:
        print("Larger than 2 and smaller than 5!")
    elif 7 < index < 12:
        print("Larger than 7 and smaller than 12!")
    else:
        if index == 4:
            print("t")
        print("Other...")
        print("(Did not match any other conditionals)")

    conditional_print(index + 1)


# Should cause a StackOverflow
# due to excessive recursion...
conditional_print(0)
