# ComPy

An efficient and simple static Python to C++ source-to-source compiler.

## Motives

The motive behind this project comes from there being almost no _native_
transpilers for Python to other languages. At some point in the process,
they eventually rely on some interpreter or Python wrapper of some sort
(if you want a Python static compiler which is already in stable versions,
check out the [mypy](https://github.com/python/mypy) /
[mypyc](https://github.com/mypyc/mypyc) projects).

The only project I managed to find which doesn't do this is the
[transpyle](https://github.com/mbdevpl/transpyle/) project, but
unfortunately it appears to have been abandoned for a few years
now. It also does not include all the Python features, which is
what I plan on including in this project.

In the end, this compiler will take Python code and output native
(no weird wrapper classes) C++ code. This will give it peak
efficiency and will offer other benefits, such as porting Python
code to C++ projects, or vice versa.

## Installation

Open a command prompt and run:
```cmd
python -m pip install -r requirements.txt
```
In future versions, we will hopefully have a `setup.py` file
to automatically install dependencies and such.

## Usage

Help menu:

```text
compy.py [-h] [-v] [-c] [-o OUTPUT] [-g] [-d] file

positional arguments:
  file                  file to compile

optional arguments:
  -h, --help            show this help message and exit
  -v, --verbose         print verbose compilation steps
  -c, --comment         adds verbose comments to the output file
  -o OUTPUT, --output OUTPUT
                        the file to output the ASM code to
  -g, --compile         compiles the output to an executable
  -d, --debug           enables debug mode for the compiler (adds mypy type checking, etc.)
```

Basic usage (compiles the Python file `examples\testcode.py`
and outputs the C++ code to the file `examples\testcode.cpp`):

```cmd
python compy.py -o examples\testcode.cpp examples\testcode.py
```

## Advanced Usage

In this section, I will primarily explain how "ported objects"
work, and how you can implement your own. Let's start with the
defenition- in ComPy, a "ported object" (or _"port"_, as it
might be called) is a snippet of code in the native langauge
(C++), which has the capability to be interacted with via the
Python code. What this all means in the end is that you can
write Python code, and you can "inject" snippets of native C++
wherever you'd like.

The benefit of this is that we can now not only interact with
our Python code by transpiling it into C++, but we can now do
the opposite by taking C++ code and "turning it into Python"
(it's not actually transpiling the native code to Python, it
simply allows for the transpiler to link these objects together
again when it's time to transpile back to native code).

That's a lot of explanation- let's see some examples. If you
view `src/pybuiltins/builtins.py`, you'll see the built-in
objects that ComPy has set up for the Python environment.
One of these objects is an example increment function called
`inc`.

```python
def inc(my_integer: int) -> int:
	"""
	Increments an integer.

	:param my_integer: The integer to increment.
	:return: The incremented value.
	"""
```

A few lines down, I then add it to the object storage like so:

```python
objs = {
    ...

    "inc": PyPortFunctionSignature(
        function=inc,
        code="return ++my_integer;"
    )

    ...
}
```

In the above snippet, I assign a Python object with a name
of `inc` to a ported function. This ported function has a
reference to the function we defined earlier, also named
`inc` (in the argument `function`). Now, ComPy knows the
function's signature (arguments and return type). Finally,
the last thing we need to specify is what the ported
function does in native code. We specify this in the `code`
parameter, by writing the code that the function will run.

Finally, in the test script `examples\test_code.py`, I call
the function (the line above it is so that PyCharm ignores it,
as I am technically calling a function that does not exist):

```python
# noinspection PyUnresolvedReferences
c = inc(c)
```

Now, when this code segment is compiled, ComPy spits out the
following snippet to the output (the valid C++ code equivalent):
```cpp
c = inc(c);
```