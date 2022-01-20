# ComPy
An efficient and simple static Python to C++ source-to-source compiler.

## Motives

The motive behind this project comes from there being almost no _native_ transpilers for Python to other languages. At some point in the process, they eventually rely on some interpreter or Python wrapper of some sort (if you want a Python static compiler which is already in stable versions, check out the [mypy](https://github.com/python/mypy) / [mypyc](https://github.com/mypyc/mypyc) projects).

The only project I managed to find which doesn't do this is the [transpyle](https://github.com/mbdevpl/transpyle/) project, but unfortunately it appears to have been abandoned for a few years now. It also does not include all the Python features, which is what I plan on including in this project.

In the end, this compiler will take Python code and output native (no weird wrapper classes) C++ code. This will give it peak efficiency and will offer other benefits, such as porting Python code to C++ projects, or vice versa.

## Installation

Open a command prompt and run:
```cmd
python -m pip install -r requirements.txt
```
In future versions, we will hopefully have a `setup.py` file to automatically install dependencies and such.

## Usage

Help menu:

```text
main.py [-h] [-v] [-c] [-o OUTPUT] file

positional arguments:
  file                  file to compile

optional arguments:
  -h, --help            show this help message and exit
  -v, --verbose         print verbose compilation steps
  -c, --comment         adds verbose comments to the output file
  -o OUTPUT, --output OUTPUT
                        the file to output the ASM code to
```

Basic usage (compiles the Python file `examples\testcode.py` and outputs the C++ code to the file `examples\testcode.cpp`):

```cmd
python main.py -o examples\testcode.cpp examples\testcode.py
```

