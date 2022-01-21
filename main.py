"""
Main script for ASManifest
"""
from argparse import ArgumentParser, FileType
from typing import IO

from src.Compiler import Compiler

print("\n[ ASManifest Compiler ]\n")

# Get arguments
parser = ArgumentParser()
# Add args
parser.add_argument('file', type=FileType(), help='file to compile')
parser.add_argument('-v', '--verbose', action='store_true', help='print verbose compilation steps')
parser.add_argument('-c', '--comment', action='store_true', help='adds verbose comments to the output file')
parser.add_argument('-o', '--output', type=FileType('w'), help='the file to output the ASM code to')
# Parse args
args = parser.parse_args()

# Get the source file
ioStream: IO = args.file
# Read the source file
print("Reading source file...")
source = ioStream.read()
# Close the file
ioStream.close()

# Send parser data to compiler
print("Parsing the file...")
c: Compiler = Compiler(args)

# Compile the file
c.parse(source)
print("Successfully parsed!")

# If there is an output file, then write there
# Otherwise, add .cpp to the file and write there
ioStream = args.output if args.output else open(args.file + '.cpp', "w")

# Compile the file to a string
print("Compiling the file...")
compiled_text: str = c.get_output()
print("Successfully compiled!")

# Write to the file
print(f"Writing to output file '{ioStream.name}'...")
ioStream.write(compiled_text)
# Close the stream
ioStream.close()
