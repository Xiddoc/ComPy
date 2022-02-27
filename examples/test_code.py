"""
Test comment.

Lots of escaped characters!
' " ` ; / % @ { } \
"""

# Assignment of type and value of constant or binary operation
a: int = (1 + 2) * 3

# Assignment of type and name with binary operation
b: int = a + 4

# Assignment of type and name
c: int = b

# Variables can be changed
# Linked function calls
# noinspection PyUnresolvedReferences
c = add(c, b)

# Built-in function calls
print("The answer is... " + str(c))

user_input: str = input("Give me input: ")

print("Testing input: " + user_input)

# Pass statement (does literally nothing)
pass


# Function declaration
def mul(x: int, y: int) -> int:
	"""
	Test function.
	"""
	# Calculate
	result: int = x * y
	# Uncomment to show that variables
	# can only be initialized once
	# result: int = 123
	return result


# Custom function usage
print(mul(3, 4))
print(mul(5, 6))
