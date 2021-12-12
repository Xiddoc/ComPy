"""
Output manager / Compiled data handler.
"""
from Names import Block


class Output:
	"""
	Output handler (saves output data).
	"""

	__output = dict[str, list[Block]]

	def __init__(self):
		# Initialize output segments
		self.__output = {"header": [], "func": [], "code": [], "footer": []}

	def header(self, code_data: str) -> Block:
		"""
		Passes code to the header segment.
		"""
		return self.__write_to("header", code_data)

	def func(self, code_data: str) -> Block:
		"""
		Passes code to the function segment.
		"""
		return self.__write_to("func", code_data)

	def code(self, code_data: str) -> Block:
		"""
		Passes code to the code segment.
		"""
		return self.__write_to("code", code_data)

	def footer(self, code_data: str) -> Block:
		"""
		Passes code to the footer segment.
		"""
		return self.__write_to("footer", code_data)

	def __write_to(self, segment: str, code_data: str) -> Block:
		"""
		Writes a snippet of data to a segment in the code.
		:param segment: The segment to write to.
		:param code_data: The code to write.
		"""
		# Create new code segment
		code_block = Block(code_data)
		# Append the code block to the current segment
		self.__output[segment].append(code_block)
		# Return a reference to the block
		return code_block

	def get_output_as_list(self) -> list[str]:
		"""
		Returns the compiled output as a list of strings.
		"""
		# Make list
		output_list: list[str] = []
		# For each section of the code
		for section in self.__output:
			# For each block of code
			for block in self.__output[section]:
				# Append the code sample to output (join the sample together)
				output_list.append(block.get_as_string())
		# Return the output
		return output_list

	def get_output(self) -> str:
		"""
		Returns the compiled output as a string.
		"""
		return "\n".join(self.get_output_as_list())
