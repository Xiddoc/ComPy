"""
Main script for ComPy.

Takes command line arguments, parses them, and
performs the logic related to it.
"""
from argparse import ArgumentParser, FileType
from platform import system
from subprocess import Popen, DEVNULL
from typing import IO
from os.path import getsize
from src.compiler.Args import Args
from src.compiler.Compiler import Compiler

print(f"""
╔═╗ ┌─┐ ┌┬┐ ╔═╗ ┬ ┬
║   │ │ │││ ╠═╝ └┬┘
╚═╝ └─┘ ┴ ┴ ╩    ┴ 
""")

# Get arguments with argument parser class
parser = ArgumentParser()
# Add args to the parser
parser.add_argument('file', type=FileType(), help='the file to compile')
parser.add_argument('-v', '--verbose', action='store_true', help='print verbose compilation steps')
parser.add_argument('-c', '--comment', action='store_true', help='adds verbose comments to the output file')
parser.add_argument('-o', '--output', type=FileType('w'), help='the file to output the ASM code to')
parser.add_argument('-g', '--compile', action='store_true', help='compiles the output to an executable')
parser.add_argument('-l', '--links', help='links ported libraries to the executable (seperate with the ; character)')

# Parse args, then create
# a singleton from arguments
Args(parser.parse_args())

# Get the source file
ioStream: IO = Args().get_args().file
# Read the source file
print("Reading source file...")
source = ioStream.read()
# Close the file
ioStream.close()

# Send parser data to compiler
print("Parsing the file...")
c: Compiler = Compiler()

# Compile the file
c.parse(source)
print("Successfully parsed!")

# If there is an output file, then write there
# Otherwise, add .cpp to the file and write there
ioStream = Args().get_args().output if Args().get_args().output else open(Args().get_args().file.name + '.cpp', "w")

# Compile the file to a string
print("Transpiling the file...")
compiled_text: str = c.compile()
print("Successfully transpiled!")

# Write to the file
print(f"Writing to output file '{ioStream.name}'...")
ioStream.write(compiled_text)
# Close the stream
ioStream.close()

# If compilation is enabled
if Args().get_args().compile:
    # Determine executable file name
    exe_path: str
    if system() == "Windows":
        exe_path = ioStream.name + ".exe"
    else:
        exe_path = ioStream.name.replace(".", "_")
    # Run G++ to compile the file
    print(f"Compiling to file '{exe_path}'...")
    Popen(["g++", "-o", exe_path, "-fconcepts", "-Os", "-s", "-fno-zero-initialized-in-bss", "-ffunction-sections", "-fdata-sections", "-Wl,--gc-sections", ioStream.name]).wait()

