"""
Main script for ComPy.

Takes command line arguments, parses them, and
performs the logic related to it.
"""
from argparse import ArgumentParser, FileType
from os.path import getsize
from platform import system
from subprocess import Popen, DEVNULL
from typing import IO
from src.compiler.Util import Util
from src.compiler.Args import Args
from src.compiler.Compiler import Compiler

# Version information, will be moved to a setup.py in the future
__version__ = 1.0
__stable__ = False

# Print the relevant version information
print(f"ComPy Release v{__version__} {'Stable' if __stable__ else 'Alpha (might have bugs/unsupported features)'}")

# Get arguments with argument parser class
parser = ArgumentParser()
# Add args to the parser
parser.add_argument('file', type=FileType(), help='the file to compile')
parser.add_argument('-o', '--output', type=FileType('w'), help='the file to output the ASM code to')
parser.add_argument('-l', '--links', help='links ported libraries to the executable (seperate with the ; character)')
parser.add_argument('-g', '--compile', action='store_true', help='compiles the output to an executable (you must have '
                                                                 'g++ installed and on the PATH)')
parser.add_argument('-c', '--compress', action='store_true', help='compresses the output executable (you must have UPX '
                                                                  'installed and on the PATH)')
parser.add_argument('-v', '--verbose', action='store_true', help='print verbose compilation steps')

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

# Compile the file to a string
print("Parsing and transpiling the file...")
compiled_text: str = Compiler.compile(source)
print("Successfully transpiled!")

# If there is an output file, then write there
# Otherwise, add .cpp to the file and write there
ioStream = Args().get_args().output if Args().get_args().output else open(Args().get_args().file.name + '.cpp', "w")
# Write to the file
print(f"Writing to output file '{ioStream.name}'...")
ioStream.write(compiled_text)
# Close the stream
ioStream.close()

# If compilation is enabled
if Args().get_args().compile:
    # Determine executable file name
    exe_path: str = ioStream.name + ".exe" if system() == "Windows" else ioStream.name.replace(".", "_")

    # Run G++ to compile the file
    print(f"Compiling to file '{exe_path}'...")
    Popen([
        # Output options and warnings
        "g++", "-o", exe_path, "-fconcepts",
        # Optimizations
        "-Os", "-s", "-fno-zero-initialized-in-bss", "-ffunction-sections", "-fdata-sections", "-Wl,--gc-sections",
        # Input file
        ioStream.name
    ]).wait()

    # Get output file size
    output_size = getsize(exe_path)
    print(f"Successfully compiled: {Util.represent_file_size(output_size)}")

    # If compression is enabled
    if Args().get_args().compress:
        # Add even more optimizations (packing)
        print(f"Packing file '{exe_path}'...")
        Popen(["upx", "-q", "--best", exe_path], stdout=DEVNULL, stderr=DEVNULL).wait()

        # Get new output file size
        packed_size = getsize(exe_path)
        print(
            f"Successfully packed: {Util.represent_file_size(output_size)} -> {Util.represent_file_size(packed_size)} "
            f"({round(100 * packed_size / output_size)}% ratio)")
