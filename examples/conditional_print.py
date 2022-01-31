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

	if index == 0:
		print("Equals to 0!")
	elif index < 3:
		print("Smaller than 3!")
	elif 5 < index < 8:
		print("Larger than 5 and smaller than 8!")
	else:
		if index == 0:
			print("t")
		print("Other...")
		print("(Did not match any other conditionals)")

	conditional_print(index + 1)


# Should cause a StackOverflow
# due to excessive recursion...
conditional_print(0)
